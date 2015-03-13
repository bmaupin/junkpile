<?php
// Constant used to tell AJAX the process needs to be continued
define( 'WPP_PROCESS_CONTINUE', 'wpp_process_continue' );

/**
 * Adds a link to the CSS for the main plugin page.
 * Simply echoes the HTML to link the stylesheet to the current document.
 */
function wpp_insert_css() {
	global $current_blog;
	$schema = ( isset($_SERVER['HTTPS']) && strtolower($_SERVER['HTTPS']) == 'on' ) ? 'https://' : 'http://'; 
	echo "<link rel='stylesheet' href='".$schema.$current_blog->domain.$current_blog->path."wp-content/mu-plugins/wpmu-prune/style.css' type='text/css' />";
}

/**
 * Gets a list of all of the blog-specific tables in the database.
 * 
 * This function gets a list of all of the blog-specific tables in the database (all tables
 * related to specific blogs, in the format [database_prefix][blog_id]_[table_name], i.e. 
 * wp_210_comments --pretty much everything but site tables).  It returns a multidimensional
 * array where the key is the blog ID, and the value of the key is a nested array containing 
 * the names of the tables associated with that blog.
 *  
 * @return array List of all blog tables.
 */
function wpp_get_blog_tables() {
	global $wpdb;
	
	$blog_tables = array();
	$query = "SHOW TABLES";
	// Get the results; it's just one column so we use get_col
	$tables = $wpdb->get_col( $query );
	foreach ( $tables as $table ) {
		// Split the table names.  The first value will be 'wp', the next, the blog ID, the third, the blog table name
		$table_values = split( '_', $table, 3 );
		// It's a blog table if the value after the first underscore is numeric.
		if ( is_numeric( $table_values[1] ) ) {
			$blog_tables[ $table_values[1] ][] = $table_values[2];
		}
	}
	
	return $blog_tables;
}

/**
 * Gets a list of all the blog IDs.
 * 
 * Gets a list of all of the blog IDs from the [database_prefix]blogs table and returns
 * a numeric array containing all of the blog IDs.
 * 
 * @return array List of all blog IDs.
 */
function wpp_get_blog_ids() {
	global $wpdb;
	
	$blog_ids = array();
	$query = "SELECT blog_id FROM {$wpdb->blogs}";
	$blog_ids = $wpdb->get_col( $query );
	
	return $blog_ids;
}

/**
 * Gets a list of all the blog attachment folders in blogs.dir.
 * 
 * Gets a list of all the blog attachment folders in wp-content/blogs.dir and returns
 * a numeric array containing all of the folders.
 * 
 * @return array List of all blog attachment folders.
 */
function wpp_get_blog_folders() {
	$blog_folders = array();
	$blog_path = constant( "ABSPATH" ) . "wp-content/blogs.dir";
	
	// taken from http://php.net/manual/en/function.readdir.php
	if ( $handle = opendir( $blog_path )) {
	
	    // loop over the directory
	    while ( false !== ( $file = readdir( $handle ))) {
	    	// skip ., .., and archived folders
	    	if ( $file != "." && $file != ".." && $file != 'archived' ) {
				$blog_folders[] = $file;
	    	}
	    }

	    closedir( $handle );
	}
	
	return $blog_folders;
}

/**
 * Gets a list of blogs that were created but never touched/used.
 * 
 * Gets a list of blogs that are unmodified within a given time of registration
 * ($max_difference) and older than a certain time ($min_age).  Puts these in a
 * numeric array containing a nested associative array where the keys are 'id' 
 * for blog ID, 'time_difference' for the amount of time a blog was modified
 * after it was registered, and 'name' for the blog name (derived from the 
 * blog_path value in the wp_blogs database with the initial and final slashes
 * stripped out).
 * 
 * @param int $max_difference The amount of maximum acceptable difference of time
 * when a blog was registered to when it was modified, in seconds.
 * @param int $min_age The minimum age of a blog in seconds to be included.
 * @return array List of untouched blogs.
 */
function wpp_get_untouched_blogs( $max_difference, $min_age ) {
	global $wpdb;
	
	$current_time = mktime();
	$untouched_blogs = array(); 
	$query = "SELECT * FROM {$wpdb->blogs} WHERE site_id = '{$wpdb->siteid}'";// ORDER BY blog_id LIMIT 0,100";
	$blog_list = $wpdb->get_results( $query, ARRAY_A );
	foreach ( $blog_list as $blog ) {
		$blog_id = $blog[ 'blog_id' ];
		
		# Don't include the main site blog in the inactive blogs list
		if( '0' == $blog_id or '1' == $blog_id ) {
			continue;
		}
		
		$last_updated = strtotime( $blog[ 'last_updated' ]);
		$registered = strtotime( $blog[ 'registered' ]);
		$time_difference = $last_updated - $registered;
		$blog_age = $current_time - $registered;
		$blog_path = $blog[ 'path' ];
		// Strip the beginning and trailing slashes from the string's path
		$blog_name = substr($blog_path, 1, -1);
		// We only want blogs older than the minimum age
		if ( $blog_age > $min_age ) {
			// Get blogs unmodified after a certain amount of time after registration
			if ( $time_difference < $max_difference ) {
//				$untouched_blogs[ $blog[ 'blog_id' ]] = $time_difference;
				$untouched_blogs[] = array(
					'id' => $blog_id,
					// For output
					'name' => $blog_name,
					// For debugging
					'time_difference' => $time_difference
				);
			}
		}
	}
	
	return $untouched_blogs;
}

/**
 * Gets a list of inactive blogs.
 * 
 * Gets the list of blogs that have been inactive (not modified or no new 
 * posts) within a given time period (in seconds) from the present 
 * ($min_inactive).  Puts these in a numeric array containing a nested 
 * associative array where the keys are 'id' for blog ID, 'inactive_time' 
 * for the amount of time (in seconds) the blog hasn't been active, 
 * 'last_updated' for the value of the 'last_updated' column in the wp_blogs
 * database for that blog in Unix timestamp format, and 'name' for the blog
 * name (derived from the blog_path value in the wp_blogs database with the
 * initial and final slashes stripped out).
 * 
 * @param int $min_inactive The minimum amount of time (in seconds) a blog has
 * to be inactive to be included in the returned array.
 * @return array List of inactive blogs.
 */
function wpp_get_inactive_blogs( $min_inactive ) {
	global $wpdb;
	
	$current_time = mktime();
	$inactive_blogs = array();
	$query = "SELECT * FROM {$wpdb->blogs} WHERE site_id = '{$wpdb->siteid}'";// ORDER BY blog_id LIMIT 0,100";
	$blog_list = $wpdb->get_results( $query, ARRAY_A );
	foreach ( $blog_list as $blog ) {
		$blog_id = $blog[ 'blog_id' ];
		
		# Don't include the main site blog in the inactive blogs list
		if( '0' == $blog_id or '1' == $blog_id ) {
			continue;
		}
		
		$last_updated = strtotime( $blog[ 'last_updated' ]);
		$blog_path = $blog[ 'path' ];
		// Strip the beginning and trailing slashes from the string's path
		$blog_name = substr($blog_path, 1, -1);
		$inactive_time = $current_time - $last_updated;
		if ( $inactive_time > $min_inactive ) {
//			$inactive_blogs[ $blog_id ] = array(
			$inactive_blogs[] = array(
				'id' => $blog_id,
				// For debugging
				'inactive_time' => $inactive_time,
				'last_updated' => $last_updated,
				// For archiving
				'name' => $blog_name
			);
		}
	}

	return $inactive_blogs;
}

function wpp_get_users( $offset = 0, $limit = '' ) {
    global $wpdb;
    
    if ( $limit != '' ) {
        $limit = "LIMIT {$offset}, ${limit}";
    }
    
    $users = array();

    $query = sprintf( "SELECT a.ID, a.user_login, b.meta_value AS
                      ldap_login FROM {$wpdb->users} a LEFT JOIN 
                      wp_usermeta b ON b.meta_key = 'ldap_login' AND 
                      a.ID = b.user_id %s", $limit );
    $user_list = $wpdb->get_results( $query, ARRAY_A );
    
    if ( $user_list != '' ) {    
        foreach ( $user_list as $user ) {
            $user_id_number = $user['ID'];
            $user_login = $user['user_login'];
            // We don't want to delete site admins
            if ( !is_site_admin( $user_login )) {
                $users[$user_id_number] = array(
                    'login' => $user_login,
                    'ldap' => $user['ldap_login'],
                );
            }
        }
    }
    return $users;
}

/* The following 8 functions have all been taken directly from 
 * /wp-admin/includes/export.php from Wordpress MU 2.9.2 only they've been 
 * given a wpp_ prefix.  The reason they're copied here at all is because for
 * some reason in the Wordpress export.php file they're all nested functions
 * within the export_wp() function.  I'm sure there's a good reason for that...
 */
function wpp_wxr_missing_parents($categories) {
	if ( !is_array($categories) || empty($categories) )
		return array();

	foreach ( $categories as $category )
		$parents[$category->term_id] = $category->parent;

	$parents = array_unique(array_diff($parents, array_keys($parents)));

	if ( $zero = array_search('0', $parents) )
		unset($parents[$zero]);

	return $parents;
}

function wpp_wxr_cdata($str) {
	if ( seems_utf8($str) == false )
		$str = utf8_encode($str);

	// $str = ent2ncr(esc_html($str));

	$str = "<![CDATA[$str" . ( ( substr($str, -1) == ']' ) ? ' ' : '') . "]]>";

	return $str;
}

function wpp_wxr_site_url() {
	global $current_site;

	// mu: the base url
	if ( isset($current_site->domain) ) {
		return 'http://'.$current_site->domain.$current_site->path;
	}
	// wp: the blog url
	else {
		return get_bloginfo_rss('url');
	}
}

function wpp_wxr_cat_name($c) {
	if ( empty($c->name) )
		return;

	echo '<wp:cat_name>' . wpp_wxr_cdata($c->name) . '</wp:cat_name>';
}

function wpp_wxr_category_description($c) {
	if ( empty($c->description) )
		return;

	echo '<wp:category_description>' . wpp_wxr_cdata($c->description) . '</wp:category_description>';
}

function wpp_wxr_tag_name($t) {
	if ( empty($t->name) )
		return;

	echo '<wp:tag_name>' . wpp_wxr_cdata($t->name) . '</wp:tag_name>';
}

function wpp_wxr_tag_description($t) {
	if ( empty($t->description) )
		return;

	echo '<wp:tag_description>' . wpp_wxr_cdata($t->description) . '</wp:tag_description>';
}

function wpp_wxr_term_name($t) {
    if ( empty($t->name) )
        return;

    echo '<wp:term_name>' . wpp_wxr_cdata($t->name) . '</wp:term_name>';
}

function wpp_wxr_term_description($t) {
    if ( empty($t->description) )
        return;

    echo '<wp:term_description>' . wpp_wxr_cdata($t->description) . '</wp:term_description>';
}

function wpp_wxr_post_taxonomy() {
	$categories = get_the_category();
	$tags = get_the_tags();
	$the_list = '';
	$filter = 'rss';

	if ( !empty($categories) ) foreach ( (array) $categories as $category ) {
		$cat_name = sanitize_term_field('name', $category->name, $category->term_id, 'category', $filter);
		// for backwards compatibility
		$the_list .= "\n\t\t<category><![CDATA[$cat_name]]></category>\n";
		// forwards compatibility: use a unique identifier for each cat to avoid clashes
		// http://trac.wordpress.org/ticket/5447
		$the_list .= "\n\t\t<category domain=\"category\" nicename=\"{$category->slug}\"><![CDATA[$cat_name]]></category>\n";
	}

	if ( !empty($tags) ) foreach ( (array) $tags as $tag ) {
		$tag_name = sanitize_term_field('name', $tag->name, $tag->term_id, 'post_tag', $filter);
		$the_list .= "\n\t\t<category domain=\"tag\"><![CDATA[$tag_name]]></category>\n";
		// forwards compatibility as above
		$the_list .= "\n\t\t<category domain=\"tag\" nicename=\"{$tag->slug}\"><![CDATA[$tag_name]]></category>\n";
	}

	echo $the_list;
}

/**
 * Taken directly from WordPress MU 2.9.2/wp-admin/includes/export.php 
 * export_wp() function.
 * Modified so that it can be called for multiple blogs.
 */
function wpp_export_blog( $blog_id, $blog_name ) {
	global $wpdb, $post_ids, $post, $wp_taxonomies, $wp_rewrite;
	
	// this needs to be called to populate $wp_taxonomies outside of the normal WP environment
	create_initial_taxonomies();
	
	define('WXR_VERSION', '1.0');
	
	// We need to make sure we're exporting the right blog
	// This code taken from /wp-admin/includes/mu.php
	if ( $blog_id != $wpdb->blogid ) {
		$switch = true;
		switch_to_blog($blog_id);
	}
	
	/* The following is necessary because the plugin actions are created before this function
	 * runs and they are created for the site blog.  This removes the rss2_head action and
	 * replaces it with a version specific to the blog we're exporting so when it's called
	 * later it will be correct.
	 */
/*	// We want to deactivate the existing rss2_head action regardless
	// @TODO: Does this need to be reset/undone after we're done with this function?
	if ( isset( $GLOBALS['wp_filter']['rss2_head'] ) ) {
		unset( $GLOBALS['wp_filter']['rss2_head'] );
		unset( $GLOBALS['merged_filters']['rss2_head'] );
	}
	// Get active plugins for current blog
	if ( get_option( 'active_plugins' ) ) {
		$current_plugins = get_option( 'active_plugins' );
	}
	// If podPress is activated for this blog, we need to readd the rss2_head action
	if ( !empty( $current_plugins ) && in_array( 'podpress/podpress.php', $current_plugins ) ) {
		$podPress = new podPress_class;
		add_action( 'rss2_head', array( &$podPress, 'rss2_head' ) );
	}
*/	
	do_action( 'export_wp' );
	
	$archive_path = constant( "ABSPATH" ) . "wp-content/blogs.dir/archived/". date('Y-m-d');
	// Built-in wordpress function to make the archive directory if it doesn't exist
	wp_mkdir_p( $archive_path );
	wp_mkdir_p( $archive_path . "/" . $blog_name );
	$filename = $archive_path . "/{$blog_name}/{$blog_name}." . date('Y-m-d') . ".xml";
	
	$where = '';
	
	// grab a snapshot of post IDs, just in case it changes during the export
	$post_ids = $wpdb->get_col("SELECT ID FROM $wpdb->posts $where ORDER BY post_date_gmt ASC");
	
	$categories = (array) get_categories('get=all');
	$tags = (array) get_tags('get=all');
	
	$custom_taxonomies = $wp_taxonomies;
	unset($custom_taxonomies['category']);
	unset($custom_taxonomies['post_tag']);
	unset($custom_taxonomies['link_category']);
	$custom_taxonomies = array_keys($custom_taxonomies);
	$terms = (array) get_terms($custom_taxonomies, 'get=all');
	
	while ( $parents = wpp_wxr_missing_parents($categories) ) {
		$found_parents = get_categories("include=" . join(', ', $parents));
		if ( is_array($found_parents) && count($found_parents) )
			$categories = array_merge($categories, $found_parents);
		else
			break;
	}
	
	// Put them in order to be inserted with no child going before its parent
	$pass = 0;
	$passes = 1000 + count($categories);
	while ( ( $cat = array_shift($categories) ) && ++$pass < $passes ) {
		if ( $cat->parent == 0 || isset($cats[$cat->parent]) ) {
			$cats[$cat->term_id] = $cat;
		} else {
			$categories[] = $cat;
		}
	}
	unset($categories);

	ob_end_flush();
	if ( 0 == ob_get_level() ) {
		ob_start();
	}	
	
echo '<?xml version="1.0" encoding="' . get_bloginfo('charset') . '"?' . ">\n";

?>
<!-- This is a WordPress eXtended RSS file generated by WordPress as an export of your blog. -->
<!-- It contains information about your blog's posts, comments, and categories. -->
<!-- You may use this file to transfer that content from one site to another. -->
<!-- This file is not intended to serve as a complete backup of your blog. -->

<!-- To import this information into a WordPress blog follow these steps. -->
<!-- 1. Log in to that blog as an administrator. -->
<!-- 2. Go to Tools: Import in the blog's admin panels (or Manage: Import in older versions of WordPress). -->
<!-- 3. Choose "WordPress" from the list. -->
<!-- 4. Upload this file using the form provided on that page. -->
<!-- 5. You will first be asked to map the authors in this export file to users -->
<!--    on the blog.  For each author, you may choose to map to an -->
<!--    existing user on the blog or to create a new user -->
<!-- 6. WordPress will then import each of the posts, comments, and categories -->
<!--    contained in this file into your blog -->

<?php the_generator('export');?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/<?php echo WXR_VERSION; ?>/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/<?php echo WXR_VERSION; ?>/"
>

<channel>
	<title><?php bloginfo_rss('name'); ?></title>
	<link><?php bloginfo_rss('url') ?></link>
	<description><?php bloginfo_rss("description") ?></description>
	<pubDate><?php echo mysql2date('D, d M Y H:i:s +0000', get_lastpostmodified('GMT'), false); ?></pubDate>
	<generator>http://wordpress.org/?v=<?php bloginfo_rss('version'); ?></generator>
	<language><?php echo get_option('rss_language'); ?></language>
	<wp:wxr_version><?php echo WXR_VERSION; ?></wp:wxr_version>
	<wp:base_site_url><?php echo wpp_wxr_site_url(); ?></wp:base_site_url>
	<wp:base_blog_url><?php bloginfo_rss('url'); ?></wp:base_blog_url>
<?php if ( $cats ) : foreach ( $cats as $c ) : ?>
	<wp:category><wp:category_nicename><?php echo $c->slug; ?></wp:category_nicename><wp:category_parent><?php echo $c->parent ? $cats[$c->parent]->name : ''; ?></wp:category_parent><?php wpp_wxr_cat_name($c); ?><?php wpp_wxr_category_description($c); ?></wp:category>
<?php endforeach; endif; ?>
<?php if ( $tags ) : foreach ( $tags as $t ) : ?>
	<wp:tag><wp:tag_slug><?php echo $t->slug; ?></wp:tag_slug><?php wpp_wxr_tag_name($t); ?><?php wpp_wxr_tag_description($t); ?></wp:tag>
<?php endforeach; endif; ?>
<?php if ( $terms ) : foreach ( $terms as $t ) : ?>
    <wp:term><wp:term_taxonomy><?php echo $t->taxonomy; ?></wp:term_taxonomy><wp:term_slug><?php echo $t->slug; ?></wp:term_slug><wp:term_parent><?php echo $t->parent ? $custom_taxonomies[$t->parent]->name : ''; ?></wp:term_parent><?php wpp_wxr_term_name($t); ?><?php wpp_wxr_term_description($t); ?></wp:term>
<?php endforeach; endif; ?>
	<?php do_action('rss2_head'); ?>
	<?php if ($post_ids) {
		global $wp_query;
		$wp_query->in_the_loop = true;  // Fake being in the loop.
		// fetch 20 posts at a time rather than loading the entire table into memory
		while ( $next_posts = array_splice($post_ids, 0, 20) ) {
			$where = "WHERE ID IN (".join(',', $next_posts).")";
			$posts = $wpdb->get_results("SELECT * FROM $wpdb->posts $where ORDER BY post_date_gmt ASC");
				foreach ($posts as $post) {
			// Don't export revisions.  They bloat the export.
			if ( 'revision' == $post->post_type )
				continue;
            setup_postdata($post);

            $is_sticky = 0;
            if ( is_sticky( $post->ID ) )
                $is_sticky = 1;

?>
<item>
<title><?php echo apply_filters('the_title_rss', $post->post_title); ?></title>
<link><?php the_permalink_rss() ?></link>
<pubDate><?php echo mysql2date('D, d M Y H:i:s +0000', get_post_time('Y-m-d H:i:s', true), false); ?></pubDate>
<dc:creator><?php echo wpp_wxr_cdata(get_the_author()); ?></dc:creator>
<?php wpp_wxr_post_taxonomy() ?>

<guid isPermaLink="false"><?php the_guid(); ?></guid>
<description></description>
<content:encoded><?php echo wpp_wxr_cdata( apply_filters('the_content_export', $post->post_content) ); ?></content:encoded>
<excerpt:encoded><?php echo wpp_wxr_cdata( apply_filters('the_excerpt_export', $post->post_excerpt) ); ?></excerpt:encoded>
<wp:post_id><?php echo $post->ID; ?></wp:post_id>
<wp:post_date><?php echo $post->post_date; ?></wp:post_date>
<wp:post_date_gmt><?php echo $post->post_date_gmt; ?></wp:post_date_gmt>
<wp:comment_status><?php echo $post->comment_status; ?></wp:comment_status>
<wp:ping_status><?php echo $post->ping_status; ?></wp:ping_status>
<wp:post_name><?php echo $post->post_name; ?></wp:post_name>
<wp:status><?php echo $post->post_status; ?></wp:status>
<wp:post_parent><?php echo $post->post_parent; ?></wp:post_parent>
<wp:menu_order><?php echo $post->menu_order; ?></wp:menu_order>
<wp:post_type><?php echo $post->post_type; ?></wp:post_type>
<wp:post_password><?php echo $post->post_password; ?></wp:post_password>
<wp:is_sticky><?php echo $is_sticky; ?></wp:is_sticky>
<?php
if ($post->post_type == 'attachment') { ?>
<wp:attachment_url><?php echo wp_get_attachment_url($post->ID); ?></wp:attachment_url>
<?php } ?>
<?php
$postmeta = $wpdb->get_results( $wpdb->prepare("SELECT * FROM $wpdb->postmeta WHERE post_id = %d", $post->ID) );
if ( $postmeta ) {
?>
<?php foreach( $postmeta as $meta ) { ?>
<wp:postmeta>
<wp:meta_key><?php echo $meta->meta_key; ?></wp:meta_key>
<wp:meta_value><?php echo $meta->meta_value; ?></wp:meta_value>
</wp:postmeta>
<?php } ?>
<?php } ?>
<?php
$comments = $wpdb->get_results( $wpdb->prepare("SELECT * FROM $wpdb->comments WHERE comment_post_ID = %d", $post->ID) );
if ( $comments ) { foreach ( $comments as $c ) { ?>
<wp:comment>
<wp:comment_id><?php echo $c->comment_ID; ?></wp:comment_id>
<wp:comment_author><?php echo wpp_wxr_cdata($c->comment_author); ?></wp:comment_author>
<wp:comment_author_email><?php echo $c->comment_author_email; ?></wp:comment_author_email>
<wp:comment_author_url><?php echo esc_url_raw( $c->comment_author_url ); ?></wp:comment_author_url>
<wp:comment_author_IP><?php echo $c->comment_author_IP; ?></wp:comment_author_IP>
<wp:comment_date><?php echo $c->comment_date; ?></wp:comment_date>
<wp:comment_date_gmt><?php echo $c->comment_date_gmt; ?></wp:comment_date_gmt>
<wp:comment_content><?php echo wpp_wxr_cdata($c->comment_content) ?></wp:comment_content>
<wp:comment_approved><?php echo $c->comment_approved; ?></wp:comment_approved>
<wp:comment_type><?php echo $c->comment_type; ?></wp:comment_type>
<wp:comment_parent><?php echo $c->comment_parent; ?></wp:comment_parent>
<wp:comment_user_id><?php echo $c->user_id; ?></wp:comment_user_id>
</wp:comment>
<?php } } ?>
	</item>
<?php } } } ?>
</channel>
</rss>
<?php
	$xml_data = ob_get_contents();
	ob_end_clean();
	file_put_contents($filename, $xml_data) or die("ERROR: Cannot write to file: {$filename}");
}


/**
 * Copy a file, or recursively copy a folder and its contents
 *
 * @author      Aidan Lister <aidan@php.net>
 * @version     1.0.1
 * @link        http://aidanlister.com/repos/v/function.copyr.php
 * @param       string   $source    Source path
 * @param       string   $dest      Destination path
 * @return      bool     Returns TRUE on success, FALSE on failure
 */
function wpp_recursive_copy($source, $dest) {
	// Check for symlinks
	if (is_link($source)) {
		return symlink(readlink($source), $dest);
	}

	// Simple copy for a file
	if (is_file($source)) {
		return copy($source, $dest);
	}

	// Make destination directory
	if (!is_dir($dest)) {
		mkdir($dest);
	}

	// Loop through the folder
	$dir = dir($source);
	while (false !== $entry = $dir->read()) {
		// Skip pointers
		if ($entry == '.' || $entry == '..') {
			continue;
		}

		// Deep copy directories
		wpp_recursive_copy("$source/$entry", "$dest/$entry");
	}

	// Clean up
	$dir->close();
	return true;
}

/**
 * Recursively deletes files and folders in a given path
 * 
 * @param string $path The path to recursively delete
 * @return bool Returns true on success, false on failure
 */
function wpp_recursive_delete( $path ) {
	// ** be very careful using this function!! **
	
	// if it's a file (or a link), simply remove it
	if ( is_file( $path ) ) {
		unlink( $path );
	
	// if it's not a file it's a directory
	} else {
		// create a file object for the directory
		$dir = dir($path);
		// if the directory's not empty go through its contents
		while ( false !== $entry = $dir->read() ) {
			// skip . and .. directories
			if ($entry == '.' || $entry == '..') {
				continue;
			}
	
			// recursively delete directory contents
			wpp_recursive_delete( "{$path}/{$entry}" );
		}
		// clean up
		$dir->close();
		// remove the directory once it's empty
		rmdir( $path );
	}
	
	return true;
}

/**
 * Prints fancy-schmancy Javascript code to show progress of an action.
 * 
 * Takes a string of an action to perform or being performed and prints 
 * Javascript that causes that action (at the bottom of this page) to be
 * performed until it's complete, updating its progress as it is processed.
 * 
 * @param string $get_action The action to perform/being performed.
 */
function wpp_ajax_progress( $get_action ) {
    $wpp_process_continue = constant( 'WPP_PROCESS_CONTINUE' );

    echo <<<JAVASCRIPT
    <script type="text/javascript">
    var makeRequest = function() {
        if (window.XMLHttpRequest) {
            var httpRequest = new XMLHttpRequest();
        } else {
            alert('Your browser is too old and will not work with this plugin. Please upgrade it and try again.');
            return;
        }
        httpRequest.onreadystatechange = function(){
            // Request is complete
            if (httpRequest.readyState === 4) {
                // Request was successful
                if (httpRequest.status === 200) {
                    document.getElementById('wpp-message').innerHTML = 
                            httpRequest.responseText.replace('{$wpp_process_continue}', '');
                    if (httpRequest.responseText.indexOf('{$wpp_process_continue}') > -1) {
                        makeRequest();
                    }
                // Request failed
                } else {
                    alert('There was a problem processing the request. Please check the logs or contact your administrator.');
                }
            }
        };
        // Send the request to the current URL (which ends up being wp-admin/wpmu-admin.php?page=wpmu-prune.php)
        httpRequest.open('GET', document.URL + '&action={$get_action}', true);
        httpRequest.send();
    };
    makeRequest();
    </script>
    <div id="wpp-message" class="updated">Please wait...</div>
JAVASCRIPT;
}

/**
 * Calculates time remaining for a process.
 * 
 * Gets the current time, the time a process was started (from a session 
 * variable), the number of items processed (session variable), the total
 * number of items to process (session variable), and calculates how much time
 * is left in the process.
 *  
 * @return string The amount of time left in the format hours:minutes:seconds
 */
function wpp_process_time() {
	$current_time = mktime();
	$total_time = $current_time - $_SESSION['process_start_time'];
	$time_per_item = $total_time / $_SESSION['items_processed'];
	$items_left = $_SESSION['items_to_process_count'] - $_SESSION['items_processed'];
	$seconds_left = $items_left * $time_per_item;
	$hours = floor( $seconds_left / 3600 );
	$seconds_left -= ( $hours * 3600 );
	$minutes = floor( $seconds_left / 60 );
	$seconds = $seconds_left - ( $minutes * 60 );
	$time_left = sprintf( "%d:%02d:%02d", $hours, $minutes, $seconds );
	
	return $time_left;
}

/**
 * Displays a message when a process is complete.
 * 
 * Takes the type of action being done and the type of item the action is done
 * to and displays a custom message when the process is complete.
 * 
 * @param $item_action The type of action being done.
 * @param $item_type The type of item the action is done to.
 */
function wpp_process_done( $item_action, $item_type ) {
	// NOTE: A change to the next line means that a corresponding change may be needed in the Javascript code in wpp_ajax_progress()
	echo "<strong>Done {$item_action} {$_SESSION['items_processed']} of {$_SESSION['items_to_process_count']} $item_type</strong><br /><br />";
	echo '<form method="post">';
	?><input type="submit" value="<?php _e('Return'); ?>" /><?php
	echo '</form>';
	exit;
}

/**
 * Displays a message when a process is complete.
 * 
 * Takes the type of action being done and the type of item the action is done
 * to and displays a custom message when the process is complete.
 * 
 * @param $item_action The type of action being done.
 * @param $item_type The type of item the action is done to.
 */
function wpp_user_process_done( $item_action, $item_type ) {
    // NOTE: A change to the next line means that a corresponding change may be needed in the Javascript code in wpp_ajax_user_progress()
    ?><p>You wish to delete all inactive users.</p>
    <p><strong>This action will delete <?php echo count( $_SESSION['deletable_users'] ); ?> (out of a total of <?php echo $_SESSION['items_to_process_count']; ?>) users.</strong></p>
    <form method="post" action="wpmu-admin.php?page=wpmu-prune.php">
      <p>Are you sure you want to do this?</p>
      <input class="wpp_boldbutton" type="submit" value="<?php _e('No'); ?>" />
      <input type="submit" name="delete_users_confirmed" value="<?php _e('Yes'); ?>" />
    </form>
    <?php
    exit;
}

function wpp_process_inactive_blogs() {
	// Set up necessary Wordpress environment stuff
	if ( !function_exists( 'wp_get_current_user' ) ) {
		require_once( ABSPATH . 'wp-includes/pluggable.php' );
	}
/*	if ( !function_exists( 'wp_revoke_user' ) ) {
		require_once( ABSPATH . 'wp-admin/includes/user.php' );
	}
*/	
	if ( !function_exists( 'wpmu_delete_blog' ) ) {
		require_once( ABSPATH . 'wp-admin/includes/mu.php' );
	}
    if ( !function_exists( 'create_initial_taxonomies' ) ) {
        require_once( ABSPATH . 'wp-includes/taxonomy.php' );
    }
/*	if ( file_exists( ABSPATH . 'wp-content/plugins/podpress/podpress.php' )) {
		if ( !class_exists( 'podPress_class' ) ) {
			require_once(ABSPATH . 'wp-content/plugins/podpress/podpress.php');
		}
	}
*/	
    
	// Get session variables
	$archive_blog = $_SESSION['archive_blog'];
	$delete_blog = $_SESSION['delete_blog'];
	
	do {
		if( 0 == count( $_SESSION['inactive_blogs'] )) {
			wpp_process_done( 'processing', 'blogs' );
		}
		
		// Get the first blog to process and remove it from the array
		$current_blog = array_shift( $_SESSION['inactive_blogs'] );
		$blog_id = $current_blog['id'];
		$blog_name = $current_blog['name'];
		
//		error_log( strftime( "%Y%m%d-%H%M%S" ) . ": " . __FILE__ . "(" . __LINE__ . "): DEBUG: blog_id: [{$blog_id}]  blog_name: [{$blog_name}]" );
	} while( '0' == $blog_id or '1' == $blog_id );  // Don't delete the main site blog

	$blog_attachment_dir = constant( "ABSPATH" ) . "wp-content/blogs.dir/{$blog_id}";
	$blog_archive_dir = constant( "ABSPATH" ) . "wp-content/blogs.dir/archived/". date('Y-m-d') . "/" . $blog_name;

	// Debugging: don't delete anything, just sleep for a couple of seconds
//	sleep(2);	
	if ( 'on' == $archive_blog ) {
//		echo 'before wpp_export_blog<br />';
		wpp_export_blog( $blog_id, $blog_name );
//		echo 'after wpp_export_blog<br />';
		if ( file_exists( $blog_attachment_dir ) ) {
			wpp_recursive_copy( $blog_attachment_dir, $blog_archive_dir );
		}
	}
	if ( 'on' == $delete_blog ) {
		wpmu_delete_blog( $blog_id, true );
		// The wpmu_delete_blog function doesn't completely remove blog attachment directories
		@rmdir($blog_attachment_dir . "/files");
		@rmdir($blog_attachment_dir);
	}

//	if( 0 == $_SESSION['processed_blogs'] ) {
//		$_SESSION['processed_blogs'] = 1;
//	} else {
		$_SESSION['items_processed'] ++;
//	}

//	Debugging; process a certain amount of blogs at a time
//	if( $_SESSION['items_processed'] >= 50) {
//		wpp_process_done( 'processing', 'blogs' );
//	}

	$time_left = wpp_process_time();

	echo "<p><strong>Processed blog {$_SESSION['items_processed']}/{$_SESSION['items_to_process_count']}</strong> &nbsp; <span style=\"font-size: 75%\">ID: {$blog_id} &nbsp;Name: {$blog_name}</span></p>";
	echo "<p>Approximate time remaining: {$time_left}</p><p>Please wait...</p>";
	echo constant( 'WPP_PROCESS_CONTINUE' );
	exit;
}

function wpp_delete_untouched_blogs() {
	// Set up necessary Wordpress environment stuff
	if ( !function_exists( 'wp_get_current_user' ) ) {
		require_once( ABSPATH . 'wp-includes/pluggable.php' );
	}
/*	if ( !function_exists( 'wp_revoke_user' ) ) {
		require_once( ABSPATH . 'wp-admin/includes/user.php' );
	}
*/	if ( !function_exists( 'wpmu_delete_blog' ) ) {
		require_once( ABSPATH . 'wp-admin/includes/mu.php' );
	}

	do {
		if( 0 == count( $_SESSION['untouched_blogs'] ) ) {
			wpp_process_done( 'deleting', 'blogs' );
		}
		// Get the first blog to delete and remove it from the array
		$current_blog = array_shift( $_SESSION['untouched_blogs'] );
		$blog_id = $current_blog['id'];
		$blog_name = $current_blog['name'];
	} while( '0' == $blog_id or '1' == $blog_id );  // Don't delete the main site blog

	// Debugging: don't delete anything, just sleep for a couple of seconds
//	sleep(2);
	
	wpmu_delete_blog( $blog_id, true );
	// The wpmu_delete_blog function doesn't completely remove blog attachment directories
	@rmdir(constant( "ABSPATH" ) . "wp-content/blogs.dir/{$blog_id}/files");
	@rmdir(constant( "ABSPATH" ) . "wp-content/blogs.dir/{$blog_id}");

	$_SESSION['items_processed'] ++;

	// Debugging; process a certain amount of blogs at a time
//	if( $_SESSION['items_processed'] >= 10) {
//		wpp_process_done( 'deleting', 'blogs' );
//	}

	$time_left = wpp_process_time();

	echo "<p><strong>Deleted blog {$_SESSION['items_processed']}/{$_SESSION['items_to_process_count']}</strong> &nbsp; <span style=\"font-size: 75%\">ID: {$blog_id} &nbsp;Name: {$blog_name}</span></p>";
	echo "<p>Approximate time remaining: {$time_left}</p><p>Please wait...</p>";
	echo constant( 'WPP_PROCESS_CONTINUE' );
	exit;
}

function wpp_process_orphaned_folders() {
	// Get session variables
	$archive_folder = $_SESSION['archive_folder'];
	$delete_folder = $_SESSION['delete_folder'];
	
	do {
		if( 0 == count( $_SESSION['orphaned_folders'] )) {
			wpp_process_done( 'processing', 'folders' );
		}
		
		// Get the first blog to process and remove it from the array
		$current_folder = array_shift( $_SESSION['orphaned_folders'] );
		
	} while( '0' == $current_folder or '1' == $current_folder );  // Don't delete the main site folder
	
	$blog_attachment_dir = constant( "ABSPATH" ) . "wp-content/blogs.dir/{$current_folder}";
	
	if ( 'on' == $archive_folder ) {
		$blog_archive_dir = constant( "ABSPATH" ) . "wp-content/blogs.dir/archived/" . date('Y-m-d') . "/" . $current_folder;
		// Built-in wordpress function to make the archive directory if it doesn't exist
		wp_mkdir_p( $blog_archive_dir );
		if ( file_exists( $blog_attachment_dir ) ) {
			wpp_recursive_copy( $blog_attachment_dir, $blog_archive_dir );
		}
	}
	if ( 'on' == $delete_folder ) {
		// ** be very careful using this function!! **
		wpp_recursive_delete( $blog_attachment_dir );
	}
	
	$_SESSION['items_processed'] ++;
	
	$time_left = wpp_process_time();

	echo "<p><strong>Processed folder {$_SESSION['items_processed']}/{$_SESSION['items_to_process_count']}</strong> &nbsp; <span style=\"font-size: 75%\">Folder: {$current_folder}</span></p>";
	echo "<p>Approximate time remaining: {$time_left}</p><p>Please wait...</p>";
	echo constant( 'WPP_PROCESS_CONTINUE' );
	exit;
}

function wpp_delete_orphaned_tables() {
	global $wpdb;
	
	do {
		if( 0 == count( $_SESSION['orphaned_tables'] )) {
			wpp_process_done( 'deleting', 'tables' );
		}
		// Get the first table to delete and remove it from the array
		$current_table = array_shift( $_SESSION['orphaned_tables'] );
	// If the current table is a main site blog table (if it starts with wp_0_ or wp_1_),
	//	get the next one.  We don't want to delete main site blog tables.
	} while( preg_match( "/^{$wpdb->base_prefix}[01]_/", $current_table ) );

	// Debugging: don't delete anything, just sleep for a couple of seconds
//	sleep(2);
	// Let the plugins know the table's being dropped in case they need to do anything
	$current_table = apply_filters( 'wpmu_drop_tables', $current_table );
	// Delete the table from the database
	$wpdb->query( "DROP TABLE IF EXISTS $current_table" );

	$_SESSION['items_processed'] ++;
	$time_left = wpp_process_time();
	
	echo "<p><strong>Deleted table {$_SESSION['items_processed']}/{$_SESSION['items_to_process_count']}</strong> &nbsp; <span style=\"font-size: 75%\">Table Name: {$current_table}</span></p>";
	echo "<p>Approximate time remaining: {$time_left}</p><p>Please wait...</p>";
	echo constant( 'WPP_PROCESS_CONTINUE' );
	exit;
}

function wpp_clean_wp_blog_versions() {
	global $wpdb;
	
	do {
		if( 0 == count( $_SESSION['blog_versions_to_delete'] )) {
			wpp_process_done( 'deleting', 'records' );
		}
		// Get the first blog ID whose record we want to delete from the blog_versions table
		$blog_id = array_shift( $_SESSION['blog_versions_to_delete'] );
	} while( '0' == $blog_id or '1' == $blog_id );  // Don't delete records for the main site blog
	
	// Debugging: don't delete anything, just sleep for a couple of seconds
//	sleep(2);
	$wpdb->query( "DELETE FROM {$wpdb->base_prefix}blog_versions WHERE blog_id = '{$blog_id}'" );
	
	$_SESSION['items_processed'] ++;
	$time_left = wpp_process_time();
	
	echo "<p><strong>Deleted record {$_SESSION['items_processed']}/{$_SESSION['items_to_process_count']}</strong> &nbsp; <span style=\"font-size: 75%\">Blog ID: {$blog_id}</span></p>";
	echo "<p>Approximate time remaining: {$time_left}</p><p>Please wait...</p>";
	echo constant( 'WPP_PROCESS_CONTINUE' );
	exit;
}

function wpp_clean_wp_groupmeta() {
	global $wpdb;
	
	do {
		if( 0 == count( $_SESSION['groupmeta_to_delete'] )) {
			wpp_process_done( 'deleting', 'sets of records' );
		}
			
		// Get the first blog ID or group whose meta we want to delete from the groupmeta table
		$key = key( $_SESSION['groupmeta_to_delete'] );
		$value = $_SESSION['groupmeta_to_delete'][$key];
		unset( $_SESSION['groupmeta_to_delete'][$key] );
		
	} while( '0' == $key or '1' == $key );  // Don't delete the main site blog group metadata
	
	// Debugging: don't delete anything, just sleep for a couple of seconds
//	sleep(2);

	if ( $value == 'blog' ) {
		// delete group metadata for deleted blogs
		$wpdb->query( "DELETE FROM {$wpdb->base_prefix}groupmeta WHERE meta_key = '{$wpdb->base_prefix}{$key}_capabilities'" );
        $wpdb->query( "DELETE FROM {$wpdb->base_prefix}groupmeta WHERE meta_key = '{$wpdb->base_prefix}{$key}_user_level'" );
	} elseif ( $value == 'group' ) {
		// delete group metadata for nonexistent groups
		$wpdb->query( "DELETE FROM {$wpdb->base_prefix}groupmeta WHERE group_name = '{$key}'" );
	}
	
	$_SESSION['items_processed'] ++;
	$time_left = wpp_process_time();
	
	echo "<p><strong>Deleted record set {$_SESSION['items_processed']}/{$_SESSION['items_to_process_count']}</strong> &nbsp; <span style=\"font-size: 75%\">Blog/group: {$key}</span></p>";
	echo "<p>Approximate time remaining: {$time_left}</p><p>Please wait...</p>";
	echo constant( 'WPP_PROCESS_CONTINUE' );
	exit;
}

function wpp_get_deletable_users() {
    // Set up necessary Wordpress environment stuff
    if ( !function_exists( 'get_blogs_of_user' ) ) {
        require_once( ABSPATH . 'wp-includes/wpmu-functions.php' );
    }
    if ( !function_exists( 'get_userdata' ) ) {
        require_once( ABSPATH . 'wp-includes/pluggable.php' );
    }
    
    if ( $_SESSION['items_processed'] >= $_SESSION['items_to_process_count'] ) {
        wpp_user_process_done( 'processing', 'users' );
    }
    
    $users = wpp_get_users( $_SESSION['items_processed'], $_SESSION['limit'] );
    
    foreach ( $users as $user_id_number => $user ) {
        // skip user id number 1 (admin)
        if ( $user_id_number == '1' ) {
            continue;
        }
        
        if ( '' == $_SESSION['delete_ldap_users'] ) {
            // don't remove LDAP users
            if ( $user['ldap'] == 'true' ) {
                continue;
            }
        }
        if ( '' == $_SESSION['delete_local_users'] ) {
            // don't remove local users
            if ( $user['ldap'] != 'true' ) {
                continue;
            }
        }
        
        // get the blog IDs of all the user's blogs
        $user_blogs = get_blogs_of_user( $user_id_number );
        
        if ( in_array( $user_id_number, $_SESSION['users_with_posts'] )) {
            continue;
        // if the user doesn't have any blogs, they're deletable
        } elseif ( count( $user_blogs ) == 0 ) {
            $_SESSION['deletable_users'][] = $user_id_number;
            continue;
        // if the user's only blog is the main blog, they're deletable
        } elseif ( count( $user_blogs ) == 1 and array_key_exists( 1, $user_blogs )) {
            $_SESSION['deletable_users'][] = $user_id_number;
            continue;
        }
    }
    
    $_SESSION['items_processed'] += $_SESSION['limit'];
    $time_left = wpp_process_time();
    
    echo "<p><strong>Processed user {$_SESSION['items_processed']}/{$_SESSION['items_to_process_count']}</strong></p>";
    echo "<p>Approximate time remaining: {$time_left}</p><p>Please wait...</p>";
    echo constant( 'WPP_PROCESS_CONTINUE' );
    exit;
}

function wpp_delete_users() {
    // Set up necessary Wordpress environment stuff
    if ( !function_exists( 'wp_get_current_user' ) ) {
        require_once( ABSPATH . 'wp-includes/pluggable.php' );
    }
    if ( !function_exists( 'wpmu_delete_user' ) ) {
        require_once( ABSPATH . 'wp-admin/includes/mu.php' );
    }

    do {
        if( 0 == count( $_SESSION['deletable_users'] ) ) {
            wpp_process_done( 'deleting', 'users' );
        }
        // Get the first user to delete and remove it from the array
        $user_id_number = array_shift ( $_SESSION['deletable_users'] );
    } while( '0' == $user_id_number or '1' == $user_id_number );  // Don't delete admin users
   
    wpmu_delete_user( $user_id_number, true );

    $_SESSION['items_processed'] ++;

    $time_left = wpp_process_time();

    echo "<p><strong>Deleted user {$_SESSION['items_processed']}/{$_SESSION['items_to_process_count']}</strong> &nbsp; <span style=\"font-size: 75%\">ID: {$user_id_number}</span></p>";
    echo "<p>Approximate time remaining: {$time_left}</p><p>Please wait...</p>";
    echo constant( 'WPP_PROCESS_CONTINUE' );
    exit;
}
?>
