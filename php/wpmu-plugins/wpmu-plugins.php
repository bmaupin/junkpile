<?php 
/*
Plugin Name: Wordpress Site Plugins
Description: Creates a Site Plugins page, much like the Site Themes page 
(wp-admin/wpmu-themes.php) that comes with Wordpress MU.  Allows admins to 
enable or disable (remove from blog Plugins page--wp-admin/plugins.php) 
plugins sitewide as well as to activate or deactivate a specific plugin for a 
specific blog (useful when plugins have been disabled).
Version: 3.1.4.1
Author: bmaupin
*/

/**
 * Adds a sub menu to the Site Admin panel.  If the currently logged in user is
 * a site admin, then this menu is created using the wpsp_main function.
 * Otherwise, nothing happens.
 */
function wpsp_addmenu() {
    /* this code adapted from ldap_addmenu function in
     * ldap/lib/wpmu_ldap_admin.functions.php file of wpmu-ldap plugin
     * (version 3.1.1)
     * wpmu-ldap.svn.sourceforge.net/viewvc/wpmu-ldap/trunk/ldap/lib/wpmu_ldap_admin.functions.php?view=markup
     */
    if (function_exists('add_submenu_page') && is_super_admin()) {
        // does not use add_options_page, because it is site-wide configuration,
        //  not blog-specific config, but side-wide
        add_submenu_page('settings.php', 'Wordpress Site Plugins', 'Site Plugins', '', basename(__FILE__), 'wpsp_main');
    }
}

/**
 * The main page of the plugin.
 * 
 * This function creates the main page of the plugin, as well as does the 
 * dirty work of actually enabling/disabling plugins sitewide or activating/
 * deactivating a specific plugin for a specific blog.
 */
function wpsp_main() {
	if( is_super_admin() == false ) {
		wp_die( __('You do not have permission to access this page.') );
	}
	
	if ( isset( $_POST['update_plugins'] )) {
		?>
		<div id="message" class="updated fade"><p><?php _e('Site plugins saved.') ?></p></div>
		<?php
		if ( is_array( $_POST['plugin'] )) {
			foreach ( $_POST['plugin'] as $plugin => $enabled ) {
				if ( 'enabled' == $enabled ) {
					$allowed_plugins[$plugin] = true;
				}
			}
			update_site_option( 'allowedplugins', $allowed_plugins );
		}
	} elseif ( isset( $_POST['activate_plugin'] ) || isset( $_POST['deactivate_plugin'] )) {
		if ( 'blog_id' == $_POST['blog_id_type'] ) {
			$blog_id = $_POST['blog'];
		} elseif ( 'blog_path' == $_POST['blog_id_type'] ) {
			global $wpdb;
			$blog_path = $_POST['blog'];
			$query = "SELECT blog_id FROM {$wpdb->blogs} WHERE {$wpdb->blogs}.domain = '{$blog_path}' OR {$wpdb->blogs}.path = '/{$blog_path}/'";
			$blog_id = $wpdb->get_var( $query );
		}	
		$plugin = $_POST['plugin_path'];
		
		// We need to make sure we switch to the correct blog before we activate/deactivate anything
		// This code taken from /wp-admin/includes/mu.php
		if ( $blog_id != $wpdb->blogid ) {
			$switch = true;
			switch_to_blog($blog_id);	
		}
		
		if ( isset( $_POST['activate_plugin'] )) {
			activate_plugin( $plugin );
			?><div id="message" class="updated fade"><p><?php _e("Plugin activated.") ?></p></div><?php
		} elseif ( isset( $_POST['deactivate_plugin'] )) {
			deactivate_plugins( $plugin );
			?><div id="message" class="updated fade"><p><?php _e("Plugin deactivated.") ?></p></div><?php
		}
	}

	/* Much of the following code taken directly from wp-admin/wpmu-themes.php
	 * of Wordpress MU 2.7.1 and 'theme' renamed to 'plugin'
	 */
	$plugins = get_plugins();
	$allowed_plugins = get_site_option( 'allowedplugins' );
	?>
	<div class="wrap">
		<form method="post">
			<h2><?php _e('Site Plugins') ?></h2>
			<p><?php _e('Enable/disable plugins site-wide.  This only adds or removes the plugin from the Plugins menu (wp-admin/plugins.php); it does not activate or deactivate plugins.') ?></p>
			<table class="widefat">
				<thead>
					<tr>
						<th style="width:15%;text-align:center;"><?php _e('Enabled') ?></th>
						<th style="width:25%;"><?php _e('Plugin') ?></th>
						<th style="width:10%;"><?php _e('Version') ?></th>
						<th style="width:60%;"><?php _e('Description') ?></th>
					</tr>
				</thead>
				<tbody id="plugins">
				<?php
				$total_plugin_count = $enabled_plugins_count = 0;
				foreach( (array) $plugins as $key => $plugin ) {
					$total_plugin_count++;
					$class = ('alt' == $class) ? '' : 'alt';
					$class1 = $enabled = $disabled = '';
					
					if( isset( $allowed_plugins[ $key ] ) == true ) {
						$enabled = 'checked="checked" ';
						$enabled_plugins_count++;
						$class1 = ' active';
					} else {
						$disabled = 'checked="checked" ';
					}				
					?>
					<tr valign="top" class="<?php echo $class.$class1; ?>">
						<td style="text-align:center;">
							<label><input name="plugin[<?php echo $key ?>]" type="radio" id="enabled_<?php echo $key ?>" value="enabled" <?php echo $enabled ?> /> <?php _e('Yes') ?></label>
							&nbsp;&nbsp;&nbsp; 
							<label><input name="plugin[<?php echo $key ?>]" type="radio" id="disabled_<?php echo $key ?>" value="disabled" <?php echo $disabled ?> /> <?php _e('No') ?></label>
						</td>
						<th scope="row" style="text-align:left;"><?php echo $plugin['Name'] ?></th> 
						<td><?php echo $plugin['Version'] ?></td>
						<td><?php echo $plugin['Description'] ?></td>
					</tr> 
				<?php } ?>
				</tbody>
			</table>
			
			<p class="submit">
				<input type='submit' name='update_plugins' value='<?php _e('Update Plugins &raquo;') ?>' /></p>
		</form>
		
		<h3><?php _e('Total')?></h3>
		<p>
			<?php printf(__('Plugins Installed: %d'), $total_plugin_count); ?>
			<br />
			<?php printf(__('Plugins Enabled: %d'), $enabled_plugins_count); ?>
		</p>
		
		<form method="post">
			<h2><?php _e('Activate/deactivate for one blog') ?></h2>
			<p><?php _e('Activate or deactivate a specific plugin for a specific blog.  This enables activation/deactivation of plugins which are disabled (removed from the Plugins menu).  Blog path can be the path of the blog (minus initial and final slashes) or a subdomain.') ?></p>
			<p class="submit">
				<select name="plugin_path">
					<?php 
					foreach ( (array) $plugins as $key => $plugin ) {
						print "<option value=\"{$key}\">{$plugin['Name']}</option>";	
					}
					?>
				</select>
				<select name="blog_id_type">
					<option value="blog_path">Blog path</option>
					<option value="blog_id">Blog ID</option>
				</select>
				<input type="text" name="blog" size="10" style="background: white; -moz-border-radius: 0px; cursor: text;" />
				<input type="submit" name="activate_plugin" value="Activate" />
				<input type="submit" name="deactivate_plugin" value="Deactivate" />
			</p>
		</form>
	</div>
	<?php
}

/**
 * Disables plugins by removing them from the blog Plugins page.
 * 
 * This function, when added to the all_plugins wordpress filter, takes the 
 * list of all plugins that is returned from the get_plugins() function, and 
 * removes plugins that are not in the list of allowed plugins (stored in the 
 * wp_sitemeta table of the wordpress database) before returning the list.  
 * $all_plugins should be an associative array where the key is the path and 
 * filename of the plugin and the value is a nested associative array, where 
 * the keys are the details of the plugin such as Name, Version, and 
 * Description, and the values are their respective values.
 * 
 * @param array $all_plugins All the plugins for the site.
 * @return array All the plugins minus the ones not in the allowedplugins site option.
 */
function wpsp_disable_plugins( $all_plugins ) {
	$allowed_plugins = get_site_option( 'allowedplugins' );
	foreach ( (array)$all_plugins as $plugin_file => $plugin_data ) {
		// Suppress errors because $allowed_plugins won't be an array if all plugins are disabled
		if ( @!array_key_exists( $plugin_file, $allowed_plugins )) {
			unset( $all_plugins[$plugin_file] );
		}
	}
	return $all_plugins;
}

// Calls the function to add this plugin to the Site Admin menu
add_action( 'network_admin_menu', 'wpsp_addmenu' );

// Adds the filter into Wordpress to disable plugins
add_filter( 'all_plugins', 'wpsp_disable_plugins' );

?>
