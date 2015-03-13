<?php 
/*
 * Start session
 * This has to be outside of main function, because main function is called 
 * from Wordpress and so the headers have already been sent.
 */
if ( !session_id() ) {
        session_start();
}

/**
 * Main function that outputs plugin choices and results.
 */
function wpp_main() {
    
    require_once( 'functions.php' );
    
    // Gives the equivalent of various units of time in seconds
    $wpp_time_units = array(
        'seconds' => 1,
        'minutes' => 60,
        'hours' => 3600,
        'days' => 86400,
        'years' => 31536000,
    );

    wpp_insert_css();
    
    if ( is_site_admin() == false ) {
        wp_die( __('<p>You do not have permission to access this page.</p>') );
    }

    if ( $_POST['process_inactive_blogs'] ) {
        global $wpdb;
        ?>
        <div id="message" class="updated">
        <?php
        
        global $current_site;
        
        $inactive_value = $_POST['inactive_value'];
        $inactive_unit = $_POST['inactive_unit'];
        $archive_blog = $_POST['archive_blog'];
        $_SESSION['archive_blog'] = $archive_blog;
        $delete_blog = $_POST['delete_blog'];
        $_SESSION['delete_blog'] = $delete_blog;
        // Calculate the minimum age of the blog in seconds
        $min_inactive = $inactive_value * $wpp_time_units[$inactive_unit];
        
        $total_blogs = $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->blogs} WHERE site_id = '{$wpdb->siteid}' ");
//      $inactive_blogs = array(
//          '26',
//          '28'
//      );
        $inactive_blogs = wpp_get_inactive_blogs( $min_inactive );
        $_SESSION['inactive_blogs'] = $inactive_blogs;
//      foreach ( $inactive_blogs as $blog_id => $values ) {
//          echo "blog: {$blog_id}, name: {$values['name']}<br />";
//      }
        
        if ( 'on' == $archive_blog && '' == $delete_blog ) {
            $action = 'archive';
        } elseif ( '' == $archive_blog && 'on' == $delete_blog ) {
            $action = 'delete';
        } elseif ( 'on' == $archive_blog && 'on' == $delete_blog ) {
            $action = 'archive and delete';
        }
        echo "<p>You wish to ".$action." all blogs inactive for ".$inactive_value." ".$inactive_unit.".</p>";
        echo "<p><strong>This action will ".$action." ".count($inactive_blogs)." (out of a total of ".$total_blogs.") blogs.</strong></p>";
        echo "</div>";
        
        // variable to hold table rows of inactive blogs
        $inactive_blogs_rows = null;
        // variable to hold table rows of previously unchecked blogs
        $unchecked_blogs_rows = null;
        // get the URL of the blog root/main blog
        $blog_root = "http://" . $current_site->domain . $current_site->path;
        
        $unchecked_blogs = get_site_option( 'unchecked_inactive_blogs' );
        $_SESSION['unchecked_inactive_blogs'] = $unchecked_blogs;
        
        foreach ( $inactive_blogs as $blog ) {
            // build the blog URL
            $blog_url = $blog_root . $blog['name'];
            // convert the last updated time from unix format
            $last_updated = date('Y-m-d', $blog['last_updated']);
            
            // create the row.  the check-column class lets us automatically check all boxes
            $this_row = 
            "<tr class = \"%s\">\n\t\t" . 
              "<th scope=\"row\" class=\"check-column\"><input type=\"checkbox\" name=\"inactive_blogs_checkbox[]\"  value=\"{$blog['id']}\" %s/></th>\n\t\t" . 
              "<td>{$blog['id']}</td>\n\t\t" . 
              "<td><a href=\"{$blog_url}\">{$blog_url}</a></td>\n\t\t" . 
              "<td>{$last_updated}</td>\n\t\t" . 
            "</tr>\n\t\t";
            
            // if the blog was previously unchecked we'll put it in a different table
            if ( !empty( $unchecked_blogs) and array_key_exists( $blog['id'], $unchecked_blogs )) {
                // alternate the class for each row so the background is a different color
                $class2 = ('alternate' == $class2) ? '' : 'alternate';
                // add the row to the table
                $unchecked_blogs_rows .= sprintf( $this_row, $class2, '');
                // don't add it to the next table
                continue;
            }
            
            // alternate the class for each row so the background is a different color
            $class = ('alternate' == $class) ? '' : 'alternate';
            // add the row to the table
            $inactive_blogs_rows .= sprintf( $this_row, $class, 'checked="yes"');
        }
        
        $inactive_blogs_table = 
        '<table class="widefat" cellspacing="0">
            <thead>
              <tr>
                <th scope="col" class="check-column"><input type="checkbox" /></th>
                <th scope="col">Blog ID</th>
                <th scope="col">Blog URL</th>
                <th scope="col">Last updated</th>
              </tr>
            </thead>
            <tbody id="inactive-blogs">
                %s
            </tbody>
          </table>';
        
        ?>
        <form method="post">
        <div class="wrap">
          <p>Are you sure you want to do this?</p>
          <input class="wpp_boldbutton" type="submit" value="<?php _e('No'); ?>" />
          <input type="submit" name="process_inactive_blogs_confirmed" value="<?php _e('Yes'); ?>" />
            <?php 
            if ( !empty( $inactive_blogs_rows )) {
                echo "<p><strong>The following blogs will be affected.  Uncheck any blogs you do not want to {$action}:</strong></p>";
                echo sprintf( $inactive_blogs_table, $inactive_blogs_rows );
            }
            if ( !empty( $unchecked_blogs_rows )) {
                echo "<p><strong>Previously unchecked blogs.  Check any blogs you want to {$action}:</strong></p>";
                echo sprintf( $inactive_blogs_table, $unchecked_blogs_rows );
            }
            ?>
        </div>
        </form>
        <?php 

//      wpp_export_blog( '19', 'bobloblawslawblog' );
//      wpp_export_blog( '21', 'steveholt' );
//      wpp_export_blog( $blog_id, $blog_name );

    } elseif ( $_POST['process_inactive_blogs_confirmed'] ) {
        $unchecked_blogs = $_SESSION['unchecked_inactive_blogs'];
        // get all of the blogs that were checked in the previous screen
        $checkboxes = $_POST['inactive_blogs_checkbox'];
        // go through the list of inactive blogs
        foreach ( $_SESSION['inactive_blogs'] as $index => $blog ) {
            // if it wasn't checked (or none were checked)
            if ( empty( $checkboxes ) or !in_array( $blog['id'], $checkboxes )) {
                // remove it from the list of blogs to be processed
                unset( $_SESSION['inactive_blogs'][$index] );
                // add it to the list of unchecked blogs if it's not there already
                if ( empty( $unchecked_blogs) or !in_array( $blog['id'], $unchecked_blogs )) {
                    $unchecked_blogs[$blog['id']] = '';
                }
            // if it was checked to be processed
            } else {
                // remove it from the list of unchecked blogs
                unset( $unchecked_blogs[$blog['id']]);
            }
        }
        
        update_site_option( 'unchecked_inactive_blogs', $unchecked_blogs );
        
        wpp_ajax_progress( 'process_inactive_blogs' );
        $_SESSION['items_processed'] = 0;
        $_SESSION['items_to_process_count'] = count( $_SESSION['inactive_blogs'] );
        $_SESSION['process_start_time'] = mktime();
        

    } elseif ( $_POST['delete_untouched_blogs'] ) {
        global $wpdb;
        ?>
        <div id="message" class="updated fade">
        <form method="post">
        <?php
        
        global $current_site;
        
        $difference_value = $_POST['difference_value'];
        $difference_unit = $_POST['difference_unit'];
        // Calculate the maximum time difference between the time the blog was registered
        //      and the time the blog was last updated in seconds
        $max_difference = $difference_value * $wpp_time_units[$difference_unit];
        
        $age_value = $_POST['age_value'];
        $age_unit = $_POST['age_unit'];
        // Calculate the minimum age of the blog in seconds
        $min_age = $age_value * $wpp_time_units[$age_unit];

        $total_blogs = $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->blogs} WHERE site_id = '{$wpdb->siteid}' ");
        $untouched_blogs = wpp_get_untouched_blogs( $max_difference, $min_age );
        $_SESSION['untouched_blogs'] = $untouched_blogs;
        
//      foreach ($untouched_blogs as $blog => $time_difference) {
//          printf('blog: %1$s, time difference: %2$d<br />', $blog, $time_difference);
//      }
        echo "<p>You wish to delete all blogs unmodified after ".$difference_value." ".$difference_unit." of registration and older than ".$age_value." ".$age_unit.".</p>";
        echo "<p><strong>This action will delete ".count($untouched_blogs)." (out of a total of ".$total_blogs.") blogs.</strong></p>";
        echo "</div>";
        
        // variable to hold table rows of untouched blogs
        $untouched_blogs_rows = null;
        // variable to hold table rows of previously unchecked blogs
        $unchecked_blogs_rows = null;
        // get the URL of the blog root/main blog
        $blog_root = "http://" . $current_site->domain . $current_site->path;
        
        $unchecked_blogs = get_site_option( 'unchecked_untouched_blogs' );
        $_SESSION['unchecked_untouched_blogs'] = $unchecked_blogs;
        
        foreach ( $untouched_blogs as $blog ) {
            // build the blog URL
            $blog_url = $blog_root . $blog['name'];
            // format the modified time difference
            $time_difference = $blog['time_difference'];
            $hours = floor( $time_difference / 3600 );
            $time_difference -= ( $hours * 3600 );
            $minutes = floor( $time_difference / 60 );
            $seconds = $time_difference - ( $minutes * 60 );
            $formatted_difference = sprintf( "%d:%02d:%02d", $hours, $minutes, $seconds );
            
            // create the row.  the check-column class lets us automatically check all boxes
            $this_row = 
            "<tr class = \"%s\">\n\t\t" . 
              "<th scope=\"row\" class=\"check-column\"><input type=\"checkbox\" name=\"untouched_blogs_checkbox[]\"  value=\"{$blog['id']}\" %s/></th>\n\t\t" . 
              "<td>{$blog['id']}</td>\n\t\t" . 
              "<td><a href=\"{$blog_url}\">{$blog_url}</a></td>\n\t\t" . 
              "<td>{$formatted_difference}</td>\n\t\t" . 
            "</tr>\n\t\t";
            
            // if the blog was previously unchecked we'll put it in a different table
            if ( !empty( $unchecked_blogs) and array_key_exists( $blog['id'], $unchecked_blogs )) {
                // alternate the class for each row so the background is a different color
                $class2 = ('alternate' == $class2) ? '' : 'alternate';
                // add the row to the table
                $unchecked_blogs_rows .= sprintf( $this_row, $class2, '');
                // don't add it to the next table
                continue;
            }
            
            // alternate the class for each row so the background is a different color
            $class = ('alternate' == $class) ? '' : 'alternate';
            // add the row to the table
            $untouched_blogs_rows .= sprintf( $this_row, $class, 'checked="yes"');
        }
        
        $untouched_blogs_table = 
        '<table class="widefat" cellspacing="0">
            <thead>
              <tr>
                <th scope="col" class="check-column"><input type="checkbox" /></th>
                <th scope="col">Blog ID</th>
                <th scope="col">Blog URL</th>
                <th scope="col">Modified after registration</th>
              </tr>
            </thead>
            <tbody id="untouched-blogs">
                %s
            </tbody>
          </table>';
        
        ?>
        <form method="post">
        <div class="wrap">
          <p>Are you sure you want to do this?</p>
          <input class="wpp_boldbutton" type="submit" value="<?php _e('No'); ?>" />
          <input type="submit" name="delete_untouched_blogs_confirmed" value="<?php _e('Yes'); ?>" />
            <?php 
            if ( !empty( $untouched_blogs_rows )) {
                echo "<p><strong>The following blogs will be affected.  Uncheck any blogs you do not want to delete:</strong></p>";
                echo sprintf( $untouched_blogs_table, $untouched_blogs_rows );
            }
            if ( !empty( $unchecked_blogs_rows )) {
                echo "<p><strong>Previously unchecked blogs.  Check any blogs you want to delete:</strong></p>";
                echo sprintf( $untouched_blogs_table, $unchecked_blogs_rows );
            }
            ?>
        </div>
        </form>
        <?php

    } elseif ( $_POST['delete_untouched_blogs_confirmed'] ) {
        $unchecked_blogs = $_SESSION['unchecked_untouched_blogs'];
        // get all of the blogs that were checked in the previous screen
        $checkboxes = $_POST['untouched_blogs_checkbox'];
        // go through the list of untouched blogs
        foreach ( $_SESSION['untouched_blogs'] as $index => $blog ) {
            // if it wasn't checked (or none were checked)
            if ( empty( $checkboxes ) or !in_array( $blog['id'], $checkboxes )) {
                // remove it from the list of blogs to be deleted
                unset( $_SESSION['untouched_blogs'][$index] );
                // add it to the list of unchecked blogs if it's not there already
                if ( empty( $unchecked_blogs) or !in_array( $blog['id'], $unchecked_blogs )) {
                    $unchecked_blogs[$blog['id']] = '';
                }
            // if it was checked to be deleted
            } else {
                // remove it from the list of unchecked blogs
                unset( $unchecked_blogs[$blog['id']]);
            }
        }
        
        update_site_option( 'unchecked_untouched_blogs', $unchecked_blogs );
        
        wpp_ajax_progress( 'delete_untouched_blogs' );
        $_SESSION['items_processed'] = 0;
        $_SESSION['items_to_process_count'] = count( $_SESSION['untouched_blogs'] );
        $_SESSION['process_start_time'] = mktime();
        
        
    } elseif ( $_POST['process_orphaned_folders'] ) {
        
        $archive_folder = $_POST['archive_folder'];
        $_SESSION['archive_folder'] = $archive_folder;
        $delete_folder = $_POST['delete_folder'];
        $_SESSION['delete_folder'] = $delete_folder;
        
        $blog_folders = wpp_get_blog_folders();
        $blog_ids = wpp_get_blog_ids();
        $_SESSION['orphaned_folders'] = array();
        
        foreach ( $blog_folders as $blog_folder ) {
            if ( !in_array( $blog_folder, $blog_ids )) {
                $_SESSION['orphaned_folders'][] = $blog_folder;
            }
        }
        
        sort( $_SESSION['orphaned_folders'] );
        $orphaned_folders_rows = '';
        foreach ( $_SESSION['orphaned_folders'] as $folder ) {
            $class = ('alternate' == $class) ? '' : 'alternate';
            $orphaned_folders_rows .= "
            <tr class=\"{$class}\" />
              <td>{$folder}</td>
            </tr>";
        }
        
        $orphaned_folders_table = 
        '<table class="widefat" cellspacing="0" style="width: 200px;">
            <thead>
              <tr>
                <th scope="col">Blog ID</th>
              </tr>
            </thead>
            <tbody id="orphaned-folders">
                ' . $orphaned_folders_rows . '
            </tbody>
          </table>';

        ?>
        <div id="message" class="updated fade">
        <?php
        if ( 'on' == $archive_folder && '' == $delete_folder ) {
            $action = 'archive';
        } elseif ( '' == $archive_folder && 'on' == $delete_folder ) {
            $action = 'delete';
        } elseif ( 'on' == $archive_folder && 'on' == $delete_folder ) {
            $action = 'archive and delete';
        }
        echo "<p>You wish to {$action} all orphaned attachment folders.</p>";
        echo "<p><strong>This action will {$action} " . count( $_SESSION['orphaned_folders'] ) . " folders.</strong></p>";
        ?>

        </div>
        <div class="wrap">
          <form method="post">
            <p>Are you sure you want to do this?</p>
            <input class="wpp_boldbutton" type="submit" value="<?php _e('No'); ?>" />
            <input type="submit" name="process_orphaned_folders_confirmed" value="<?php _e('Yes'); ?>" />
          </form>
          <?php
            if ( !empty( $orphaned_folders_rows )) {
                echo '<p>The attachment folders of the following blogs will be affected:</p>';
                echo $orphaned_folders_table;
            }
          ?>
        </div>
        <?php 

    } elseif ( $_POST['process_orphaned_folders_confirmed'] ) {
        wpp_ajax_progress( 'process_orphaned_folders' );
        $_SESSION['items_processed'] = 0;
        $_SESSION['items_to_process_count'] = count( $_SESSION['orphaned_folders'] );
        $_SESSION['process_start_time'] = mktime();

        
    } elseif ( $_POST['delete_orphaned_tables'] ) {
        global $wpdb;
        ?>
        <div id="message" class="updated fade">
        <?php
        $blog_tables = wpp_get_blog_tables();
        $blog_ids = wpp_get_blog_ids();
        // Clean this out in case there's something in it
        $_SESSION['orphaned_tables'] = array();
        // Go through each blog ID of existing tables
        foreach ( $blog_tables as $blog_id => $tables ) {   
            // We don't want to delete any main site blog tables
            if( '0' == $blog_id or '1' == $blog_id ) {
                continue;
            }
            // If the blog ID isn't in the list of blog IDs
            if ( !in_array( $blog_id, $blog_ids ) ) {
                foreach ( $tables as $table ) {
                    // Add that table to the list/array of tables to be dropped
                    $_SESSION['orphaned_tables'][] = $wpdb->base_prefix . $blog_id . '_' . $table;
                }
            }
        }

        echo "<p>You wish to delete all orphaned tables.</p>";
        echo "<p><strong>This action will delete " . count( $_SESSION['orphaned_tables'] ) . " tables.</strong></p>";
        ?>
        </div>
        <form method="post">
        <div class="wrap">
          <p>Are you sure you want to do this?</p>
          <input class="wpp_boldbutton" type="submit" value="<?php _e('No'); ?>" />
          <input type="submit" name="delete_orphaned_tables_confirmed" value="<?php _e('Yes'); ?>" />
        </div>
        </form>
        <?php
    
    } elseif ( $_POST['delete_orphaned_tables_confirmed'] ) {
        wpp_ajax_progress( 'delete_orphaned_tables' );
        $_SESSION['items_processed'] = 0;
        $_SESSION['items_to_process_count'] = count( $_SESSION['orphaned_tables'] );
        $_SESSION['process_start_time'] = mktime();

        
    } elseif ( $_POST['clean_wp_groupmeta'] ) {
        global $wpdb;
        
        /* update the database with the value of the ldap group base given in
         * the POST data from the form
         */ 
        update_site_option( 'wpp_group_base', $_POST['ldap_group_base'] );
        
        $delete_records_count = 0;
        $_SESSION['groupmeta_to_delete'] = array();
        $blog_ids = wpp_get_blog_ids();
        
        $query = "SELECT group_name, meta_key FROM {$wpdb->base_prefix}groupmeta ORDER BY meta_key";
        $groupmeta = $wpdb->get_results( $query );
        // strings to hold rows of groupmeta to be deleted
        $groupmeta_blogs_rows = '';
        $groupmeta_groups_rows = '';
        
        // set up stuff for connecting to LDAP
        $ldapServerAddr    = get_site_option( 'ldapServerAddr' );
        $ldapServerCN      = get_site_option( 'ldapServerCN' );
        $ldapServerPass    = get_site_option( 'ldapServerPass' );
        $ldapServerPort    = get_site_option( 'ldapServerPort' );
        $ldapEnableSSL     = get_site_option( 'ldapEnableSSL' );
        $ldapSearchBase    = $_POST['ldap_group_base'];
        
        $ldapString = array( $ldapServerAddr, $ldapSearchBase, $ldapServerCN, $ldapServerPass, $ldapServerPort, $ldapEnableSSL );
        $server = new LDAP_ro( $ldapString );
        $server->DebugOff();
        // connect to LDAP
        $server->Dock();
        
        // parse each row of the groupmeta table
        foreach ( $groupmeta as $meta ) {
            // first see if the group is in LDAP
            $group = $meta->group_name;
            $server->SetSearchCriteria("(&(objectClass=groupOfNames)(cn={$group}))", array( "cn" ) );
            $server->Search();
            $result = $server->info[0]["cn"][0];
            
            // if the group isn't in LDAP
            if ( $result != $group ) {
                $delete_records_count++;
                if ( !array_key_exists( $group, $_SESSION['groupmeta_to_delete'] )) {
                    // add the group to the list of metadata to be deleted
                    $_SESSION['groupmeta_to_delete'][$group] = 'group';
                    // create a row for the table of metadata to be deleted
                    $group_class = ('alternate' == $group_class) ? '' : 'alternate';
                    $groupmeta_groups_rows .= "
                    <tr class=\"{$group_class}\" />
                      <td>{$group}</td>
                    </tr>";
                }
            // if the group is in LDAP, next see if the blog exists
            } else {
            
                $key_values = split( '_', $meta->meta_key, 3 );
                // Split the meta_keys.  The first value will be 'wp', the next, the blog ID, the third, 'capabilities' or 'user_level'
                $blog_id = $key_values[1];
                // If the blog ID isn't in the list of blog IDs
                if ( !in_array( $blog_id, $blog_ids )) {
                    $delete_records_count++;
                    // If it isn't already in the list of blog IDs to be deleted from the groupmeta table
                    if ( !array_key_exists( $blog_id, $_SESSION['groupmeta_to_delete'] ) ) {
                        // Add that blog ID to a list to be deleted from the groupmeta table
                        $_SESSION['groupmeta_to_delete'][$blog_id] = 'blog';
                        // create a row for the table of metadata to be deleted
                        $blog_class = ('alternate' == $blog_class) ? '' : 'alternate';
                        $groupmeta_blogs_rows .= "
                        <tr class=\"{$blog_class}\" />
                          <td>{$blog_id}</td>
                        </tr>";
                    }
                }
            }
        }
        // disconnect the LDAP connection
        $server->Disconnect();
        
        // table template, minus the width, heading, and rows
        $groupmeta_table = 
        '<table class="widefat" cellspacing="0" style="width: %spx;">
            <thead>
              <tr>
                <th scope="col">%s</th>
              </tr>
            </thead>
            <tbody>
                %s
            </tbody>
          </table>';
        ?>
        <div id="message" class="updated">
        <?php
        echo '<p>You wish to delete all records from the wp_groupmeta table belonging to deleted blogs.</p>';
        echo "<p><strong>This action will delete {$delete_records_count} records.</strong></p>"; 
        ?>
        </div>
        <div class="wrap">
          <form method="post">
            <p>Are you sure you want to do this?</p>
            <input class="wpp_boldbutton" type="submit" value="<?php _e('No'); ?>" />
            <input type="submit" name="clean_wp_groupmeta_confirmed" value="<?php _e('Yes'); ?>" />
          </form>
        <?php
            // show tables for metadata to be deleted (if there is metadata to be deleted)
            if ( !empty( $groupmeta_groups_rows )) {
                echo '<p>The groupmeta for the following nonexistent groups will be removed:</p>';
                echo sprintf( $groupmeta_table, '500', 'Group', $groupmeta_groups_rows );
            }
            if ( !empty( $groupmeta_blogs_rows )) {
                echo '<p>The groupmeta for the following deleted blogs will be removed:</p>';
                echo sprintf( $groupmeta_table, '200', 'Blog ID', $groupmeta_blogs_rows );
            }
        ?>
        </div>
        <?php       
        
    } elseif ( $_POST['clean_wp_groupmeta_confirmed'] ) {
        wpp_ajax_progress( 'clean_wp_groupmeta' );
        $_SESSION['items_processed'] = 0;
        $_SESSION['items_to_process_count'] = count( $_SESSION['groupmeta_to_delete'] );
        $_SESSION['process_start_time'] = mktime();

        
    } elseif ( $_POST['clean_wp_blog_versions'] ) {
        global $wpdb;
        ?>
        <div id="message" class="updated">
        <?php
        $delete_records_count = 0;
        $_SESSION['blog_versions_to_delete'] = array();
        $blog_ids = wpp_get_blog_ids();
        $query = "SELECT blog_id FROM {$wpdb->base_prefix}blog_versions ORDER BY blog_id";
        // Put all the values of the blog_id column in the blog_versions table into $blog_versions_blog_ids
        $blog_versions_blog_ids = $wpdb->get_col( $query );
        foreach ( $blog_versions_blog_ids as $blog_versions_blog_id ) {
            // If the blog ID isn't in the list of sitewide blog IDs
            if ( !in_array( $blog_versions_blog_id, $blog_ids )) {
                $delete_records_count++;
                // Add that blog ID to a list to be deleted from the blog_versions table
                $_SESSION['blog_versions_to_delete'][] = $blog_versions_blog_id;
            }
        }

        echo '<p>You wish to delete all records from the wp_blog_versions table belonging to deleted blogs.</p>';
        echo "<p><strong>This action will delete {$delete_records_count} records.</strong></p>"; 
        ?>
        </div>
        <form method="post">
        <div class="wrap">
          <p>Are you sure you want to do this?</p>
          <input class="wpp_boldbutton" type="submit" value="<?php _e('No'); ?>" />
          <input type="submit" name="clean_wp_blog_versions_confirmed" value="<?php _e('Yes'); ?>" />
        </div>
        </form>
        <?php       
        
    } elseif ( $_POST['clean_wp_blog_versions_confirmed'] ) {
        wpp_ajax_progress( 'clean_wp_blog_versions' );
        $_SESSION['items_processed'] = 0;
        $_SESSION['items_to_process_count'] = count( $_SESSION['blog_versions_to_delete'] );
        $_SESSION['process_start_time'] = mktime();

    
    } elseif ( $_POST['delete_users'] ) {
        global $current_site, $wpdb;
        
        $blog_ids = wpp_get_blog_ids();
        $users_with_posts = array();
        
        foreach ( $blog_ids as $blog_id ) {
            // get all of the authors of the posts for each blog
            $query = sprintf( "SELECT DISTINCT post_author FROM wp_%s_posts", 
                              $blog_id );
            $post_authors = $wpdb->get_col( $query );
            
            foreach ( $post_authors as $post_author ) {
                if ( !in_array( $post_author, $users_with_posts )) {
                    $users_with_posts[] = $post_author;
                }
            }
        }
        
        $_SESSION['users_with_posts'] = $users_with_posts;
        $_SESSION['delete_ldap_users'] = $_POST['delete_ldap_users'];
        $_SESSION['delete_local_users'] = $_POST['delete_local_users'];
        $_SESSION['deletable_users'] = array();
        
        wpp_ajax_progress( 'get_deletable_users' );
        $_SESSION['items_processed'] = 0;
        $_SESSION['items_to_process_count'] = $wpdb->get_var("SELECT COUNT(id) FROM {$wpdb->users}");
        $_SESSION['process_start_time'] = mktime();
        $_SESSION['offset'] = 0;
        // process this many users at a time
        $_SESSION['limit'] = 10;
    
    } elseif ( $_POST['delete_users_confirmed'] ) {
        wpp_ajax_progress( 'delete_users' );
        $_SESSION['items_processed'] = 0;
        $_SESSION['items_to_process_count'] = count( $_SESSION['deletable_users'] );
        $_SESSION['process_start_time'] = mktime();

        
    } else {

//****************************************************************************
// CODE TO SHOW MAIN PLUGIN PAGE
        global $wpp_version;
        
        ?>
        <!-- Script to display options when a choice is clicked on -->
        <script type="text/javascript">
        function showHideElement(id) {
            if (document.getElementById) {
                obj = document.getElementById(id);
                if (obj.style.display == "none") {
                    obj.style.display = "block";
                } else {
                    obj.style.display = "none";
                }
            }
        }
        </script>
        <div class="wrap">

        <h2>Wordpress MU Prune v <?php echo $wpp_version; ?></h2>
        <p>Cleans up Wordpress MU by removing inactive and untouched (never used) blogs and associated tables and records.<br /></p>

        <form method="post" class="wpp_form">
            <div class="wpp_choice" onclick="showHideElement('process_inactive_blogs_options')"><strong>Archive and/or delete inactive blogs</strong></div>
            <div id="process_inactive_blogs_options" style="display: none;">
                <p><i>Archive and/or delete blogs not modified or with no new posts within a specified length of time.</i><br /></p>
                <p>For blogs not modified within the last <input type="text" name="inactive_value" value="1"/>
                <select name="inactive_unit">
                <?php foreach ( $wpp_time_units as $time_unit => $time_value ) {
                    if ( 'years' == $time_unit ) {  // Sets the default value
                        echo '<option value = "'.$time_unit.'" selected="selected">'.$time_unit.'</option>';
                    } else {
                        echo '<option value = "'.$time_unit.'">'.$time_unit.'</option>';
                    } 
                } ?>
                </select>, do the following:<br />
                <input type="checkbox" name="archive_blog" checked="yes" /> Archive<br />
                <input type="checkbox" name="delete_blog" /> Delete<br />

                <div class="submit">
                    <input type="submit" name="process_inactive_blogs" value="<?php _e('Go'); ?> &raquo;" />
                </div>
            </div>
        </form>
        
        <form method="post" class="wpp_form">
            <div class="wpp_choice" onclick="showHideElement('delete_untouched_blogs_options')"><strong>Delete untouched blogs</strong></div>
            <div id="delete_untouched_blogs_options" style="display: none;">
                <p><i>Delete blogs unmodified a certain time after registration.</i><br /></p>
                <p>Delete blogs unmodified after <input type="text" name="difference_value" value="60" />
                <select name="difference_unit">
                    <?php foreach ( $wpp_time_units as $time_unit => $time_value ) {
                        if ( 'seconds' == $time_unit ) {  // Sets the default value
                            echo '<option value = "'.$time_unit.'" selected="selected">'.$time_unit.'</option>';
                        } else {
                            echo '<option value = "'.$time_unit.'">'.$time_unit.'</option>';
                        } 
                    } ?>
                </select>
                of registration<br />
                &nbsp; &nbsp;and older than <input type="text" name="age_value" value="30" />
                <select name="age_unit">
                <?php foreach ( $wpp_time_units as $time_unit => $time_value ) {
                    if ( 'days' == $time_unit ) {  // Sets the default value
                        echo '<option value = "'.$time_unit.'" selected="selected">'.$time_unit.'</option>';
                    } else {
                        echo '<option value = "'.$time_unit.'">'.$time_unit.'</option>';
                    } 
                } ?>
                </select>
             
                <div class="submit">
                    <input type="submit" name="delete_untouched_blogs" value="<?php _e('Go'); ?> &raquo;" />
                </div>
            </div>
        </form>

        <form method="post" class="wpp_form">
            <div class="wpp_choice" onclick="showHideElement('process_orphaned_folders_options')"><strong>Archive and/or delete orphaned attachment folders</strong></div>
            <div id="process_orphaned_folders_options" style="display: none;">
                <p><i>Archive and/or delete attachment folders left behind when the blogs they belonged to were deleted.</i><br /></p>
                <input type="checkbox" name="archive_folder" checked="yes" /> Archive<br />
                <input type="checkbox" name="delete_folder" /> Delete<br />

                <div class="submit">
                    <input type="submit" name="process_orphaned_folders" value="<?php _e('Go'); ?> &raquo;" />
                </div>
            </div>
        </form>
        
        <form method="post" class="wpp_form">
            <div class="wpp_choice" onclick="showHideElement('delete_orphaned_tables_options')"><strong>Delete orphaned tables</strong></div>
            <div id="delete_orphaned_tables_options" style="display: none;">
                <p><i>Delete tables left behind when the blogs they belonged to were deleted.</i><br /></p>

                <div class="submit">
                    <input type="submit" name="delete_orphaned_tables" value="<?php _e('Go'); ?> &raquo;" />
                </div>
            </div>
        </form>
        
        <form method="post" class="wpp_form">
            <div class="wpp_choice" onclick="showHideElement('clean_wp_blog_versions_options')"><strong>Clean up wp_blog_versions table</strong></div>
            <div id="clean_wp_blog_versions_options" style="display: none;">
                <p><i>Delete records from the wp_blog_versions table belonging to deleted blogs.</i><br /></p>

                <div class="submit">
                    <input type="submit" name="clean_wp_blog_versions" value="<?php _e('Go'); ?> &raquo;" />
                </div>
            </div>
        </form>
        
        <?php
        /* only show the option to clean up group metadata if the ldap groups 
         * metadata table exists
         */
        global $wpdb;
        $result = $wpdb->get_var( "SHOW TABLES LIKE '{$wpdb->base_prefix}groupmeta'" );
        
        if ( $result != '' ):
            $ldap_groups = get_site_option('ldapGroups');
 
            if ( $ldap_groups != '' ) {
                // first try to get the value from the site option put there by this plugin
                $ldap_group_base = get_site_option('wpp_group_base');
                
                if ( $ldap_group_base == '' ) {
                    // then try to get it from the site option put there by the LDAP groups plugin
                    $ldap_group_base = get_site_option('ldapGroupBase');
                    if ( $ldap_group_base == '' ) {
                        // lastly, set a default value
                        $ldap_group_base = 'ou=groups,dc=example,dc=com';
                    }
                }
            }
        ?>
        
        <form method="post" class="wpp_form">
            <div class="wpp_choice" onclick="showHideElement('clean_wp_groupmeta_options')"><strong>Clean up wp_groupmeta table</strong></div>
            <div id="clean_wp_groupmeta_options" style="display: none;">
                <p><i>Delete records from the wp_groupmeta table belonging to deleted blogs or nonexistent groups.</i><br /></p>
                
                <table class="form-table">
                  <tr valign="top">
                    <th scope="row">LDAP Group Base:</th>
                    <td>
                     <input type='text' name='ldap_group_base' value='<?php echo $ldap_group_base ?>' style='width: 300px;' />
                     <br/>
                     The starting base dn for groups in LDAP.<br/>
                     Ex: ou=groups,dc=example,dc=com
                    </td>
                  </tr>
                </table>
                
                <div class="submit">
                    <input type="submit" name="clean_wp_groupmeta" value="<?php _e('Go'); ?> &raquo;" />
                </div>
            </div>
        </form>
        
        <?php endif; ?>
        
        <form method="post" class="wpp_form">
            <div class="wpp_choice" onclick="showHideElement('delete_inactive_users_options')"><strong>Delete inactive users</strong></div>
            <div id="delete_inactive_users_options" style="display: none;">
                <p><i>Delete non-admin users who aren't associated with any blogs (or who are only associated with the main blog) and who have no posts.</i><br /></p>
                <input type="checkbox" name="delete_ldap_users" checked="yes" /> Delete inactive LDAP users<br />
                <input type="checkbox" name="delete_local_users" /> Delete inactive local users<br />
                    
                <div class="submit">
                    <input type="submit" name="delete_users" value="<?php _e('Go'); ?> &raquo;" />
                </div>
            </div>
        </form>
        
        </div>
        
        <!-- This option is disabled because LDAP isn't being cleaned of users and so we don't have any to remove
        <form method="post" class="wpp_form">
            <div class="wpp_choice" onclick="showHideElement('delete_inactive_users_options')"><strong>Delete inactive users</strong></div>
            <div id="delete_inactive_users_options" style="display: none;">
                <p><i>Delete users who are inactive and/or aren't in LDAP.</i><br /></p>
                <p>Delete users:<br />
                <input type="checkbox" name="delete_inactive_users" /> who are inactive for <input type="text" name="inactive_value" />
                <select name="inactive_unit">
                <?php foreach ( $wpp_time_units as $time_unit => $time_value ) {
                    if ( 'years' == $time_unit ) {  // Sets the default value
                        echo '<option value = "'.$time_unit.'" selected="selected">'.$time_unit.'</option>';
                    } else {
                        echo '<option value = "'.$time_unit.'">'.$time_unit.'</option>';
                    } 
                } ?>
                </select><br />
                <input type="checkbox" name="delete_ldap_users" /> who are no longer in LDAP (but were at one time)<br />
                    
                <div class="submit">
                    <input type="submit" name="delete_users" value="<?php _e('Go'); ?> &raquo;" />
                </div>
            </div>
        </form>
        -->
        <?php
    }
}
?>
