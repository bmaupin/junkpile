<?php
/*
Plugin Name: Wordpress MU Prune
Plugin URI: https://github.com/bmaupin/graveyard/tree/master/php/wpmu-prune
Description: Cleans up Wordpress MU by removing inactive and untouched (never 
used) blogs and associated tables and records.
Version: 2.9.0
Author: bmaupin
*/

// The current version of this plugin.  Should be the same as "Version: "
// above.  If not, whichever version is newer is probably accurate.
$wpp_version = '2.9.0';

/**
 * Adds a sub menu to the Site Admin panel.  If the currently logged in user is
 * a site-admin, then this menu is created using the wpp_main function.
 * Otherwise, nothing happens.
 */
function wpp_addmenu() {
	$objCurrUser = wp_get_current_user();
	$objUser = wp_cache_get($objCurrUser->id, 'users');
	if ( function_exists ( 'add_submenu_page' ) && is_site_admin( $objUser->user_login ) ) {
		// does not use add_options_page, because it is site-wide configuration,
		//  not blog-specific config, but side-wide
		add_submenu_page('wpmu-admin.php', 'Wordpress MU Prune', 'WPMU Prune', 9, basename(__FILE__), 'wpp_main');
		require_once( 'wpmu-prune/main.php' );
	}
}

if ( function_exists ( 'add_action' )) {
    // Calls the function to add this plugin to the Site Admin menu
    add_action( 'admin_menu', 'wpp_addmenu' );
}

if ( !empty( $_GET['action'] )) {
	require_once( 'wpmu-prune/functions.php' );
	require_once( 'wpmu-prune/main.php' );

	if ( 'delete_untouched_blogs' == $_GET['action'] ) {
		wpp_delete_untouched_blogs();
	} elseif ( 'process_inactive_blogs' == $_GET['action'] ) {
		// Set up necessary Wordpress environment stuff
		global $wp_query, $wp_rewrite;
		$wp_the_query =& new WP_Query();
		$wp_query     =& $wp_the_query;
		$wp_rewrite   =& new WP_Rewrite();
		wpp_process_inactive_blogs();
	} elseif ( 'process_orphaned_folders' == $_GET['action'] ) {
		wpp_process_orphaned_folders();
	} elseif ( 'delete_orphaned_tables' == $_GET['action'] ) {
		wpp_delete_orphaned_tables();
	} elseif ( 'clean_wp_groupmeta' == $_GET['action'] ) {
		wpp_clean_wp_groupmeta();
	} elseif ( 'clean_wp_blog_versions' == $_GET['action'] ) {
		wpp_clean_wp_blog_versions();
	} elseif ( 'get_deletable_users' == $_GET['action'] ) {
	    wpp_get_deletable_users();
    } elseif ( 'delete_users' == $_GET['action'] ) {
        wpp_delete_users();
	}
}

?>
