import re

# from enum import Enum # annoying to get the value.
FORUM_LINK = "https://atelier801.com/"

class CookieState:
	login       = 0 # Get all cookies
	after_login = 1 # Get all cookies after login
	action      = 2 # ^, except the ones in the `NonActionCookie` enum

class NonActionCookie:
	JSESSIONID = True
	token      = True
	token_date = True

class Separator:
	cookie     = '; '
	forum_data = '§#§'
	file       = '\r\n'

class ForumUri:
	acc                        = "account"
	add_favorite               = "add-favourite"
	add_friend                 = "add-friend"
	answer_conversation        = "answer-conversation"
	answer_poll                = "answer-forum-poll"
	answer_private_poll        = "answer-conversation-poll"
	answer_topic               = "answer-topic"
	blacklist                  = "blacklist"
	close_discussion           = "close-discussion"
	conversation               = "conversation"
	conversations              = "conversations"
	create_dialog              = "create-dialog"
	create_discussion          = "create-discussion"
	create_section             = "create-section"
	create_topic               = "create-topic"
	disconnection              = "deconnexion"
	edit                       = "edit"
	edit_message               = "edit-topic-message"
	edit_section               = "edit-section"
	edit_section_permissions   = "edit-section-permissions"
	edit_topic                 = "edit-topic"
	element_id                 = "ie"
	favorite_id                = "fa"
	favorite_topics            = "favorite-topics"
	favorite_tribes            = "favorite-tribes"
	friends                    = "friends"
	get_cert                   = "get-certification"
	identification             = "identification"
	ignore_user                = "add-ignored"
	images_gallery             = "gallery-images-ajax"
	index                      = "index"
	invite_discussion          = "invite-discussion"
	kick_member                = "kick-discussion-member"
	leave_discussion           = "quit-discussion"
	like_message               = "like-message"
	login                      = "login"
	manage_message_restriction = "manage-selected-topic-messages-restriction"
	message_history            = "tribulle-frame-topic-message-history"
	moderate                   = "moderate-selected-topic-messages"
	move_all_conversations     = "move-all-conversations"
	move_conversation          = "move-conversations"
	new_dialog                 = "new-dialog"
	new_discussion             = "new-discussion"
	new_poll                   = "new-forum-poll"
	new_private_poll           = "new-private-poll"
	new_section                = "new-section"
	new_topic                  = "new-topic"
	poll_id                    = "po"
	posts                      = "posts"
	profile                    = "profile"
	quote                      = "citer"
	remove_avatar              = "remove-profile-avatar"
	remove_blacklisted         = "remove-ignored"
	remove_favorite            = "remove-favourite"
	remove_image               = "remove-user-image"
	remove_logo                = "remove-tribe-logo"
	reopen_discussion          = "reopen-discussion"
	report                     = "report-element"
	search                     = "search"
	section                    = "section"
	set_cert                   = "set-certification"
	set_email                  = "set-email"
	set_pw                     = "set-password"
	staff                      = "staff-ajax"
	topic                      = "topic"
	topics_started             = "topics-started"
	tracker                    = "dev-tracker"
	tribe                      = "tribe"
	tribe_forum                = "tribe-forum"
	tribe_history              = "tribe-history"
	tribe_members              = "tribe-members"
	update_avatar              = "update-profile-avatar"
	update_parameters          = "update-user-parameters"
	update_profile             = "update-profile"
	update_section             = "update-section"
	update_section_permissions = "update-section-permissions"
	update_topic               = "update-topic"
	update_tribe               = "update-tribe"
	update_tribe_message       = "update-tribe-greeting-message"
	update_tribe_parameters    = "update-tribe-parameters"
	upload_image               = "upload-user-image"
	upload_logo                = "update-tribe-logo"
	user_images                = "user-images-home"
	user_images_grid           = "user-images-grid-ajax"
	view_user_image            = "view-user-image"

class HtmlChunk:
	admin_name                = re.compile(r'cadre-type-auteur-admin">(.+?)</span>')
	blacklist_name            = re.compile(r'cadre-ignore-nom">(.+?)</span>')
	community                 = re.compile(r'pays/(..)\.png')
	conversation_icon         = re.compile(r'cadre-sujet-titre">(.+?)</span>\s+</td>\s+</tr>\s+</table>')
	created_topic_data        = re.compile(r'href="(topic\?f=\d+&t=\d+).+?".+?>\s+([^>]+)\s+</a>.+?\2.+?m(\d+)')
	date                      = re.compile(r'(\d+/\d+/\d+)')
	edition_timestamp         = re.compile(r'cadre-message-dates.+?(\d+)')
	empty_section             = re.compile(r'<div class="aucun-resultat">Empty</div>')
	favorite_topics           = re.compile(r'<td rowspan="2">(.+?)</td>\s+<td rowspan="2">')
	greeting_message          = re.compile(r'<h4>Greeting message</h4> (.+)$')
	hidden_value              = re.compile(r'<input type="hidden" name="{}" value="(\d+)"/?>')
	image_id                  = re.compile(r'?im=(\w+)"')
	last_post                 = re.compile(r'<a href="(topic\?.+?)".+?>\s+(.+?)\s+</a></li>.+?\1.+?#m(\d+)">')
	message                   = re.compile(r'cadre_message_sujet_(\d+)">\s+<div id="m\d"(.+?</div>\s+</div>\s+</div>)')
	message_content           = re.compile(r'"\s_message_\d" .+?>(.+?)<')
	message_data              = re.compile(r'class="coeur".+?(\d+).+?message_\d+">(.+?)</div>\s+</div>')
	message_history_log       = re.compile(r'class="hidden"> (.+?) </div>')
	message_html              = re.compile(r'Message</a></span> :\s+(.+?)\s*</div>\s+</td>\s+</tr>')
	message_post_id           = re.compile(r'numero-message".+?#(\d+)')
	moderated_message         = re.compile(r'cadre-message-modere-texte">.+?by ([^,]+)[^:]*:?\s*(.*)\s*\]<')
	ms_time                   = re.compile(r'data-afficher-secondes.+?>(\d+)')
	navigation_bar            = re.compile(r'"barre-navigation.+?>(.+?)</ul>')
	navigaton_bar_sec_content = re.compile(r'^<(.+)>\s*(.+)\s*$')
	navigaton_bar_sections    = re.compile(r'<a.+?href="(.+?)".+?>\s*(.+?)\s*</a>')
	nickname                  = re.compile(r'(\S+)<span class="nav-header-hashtag">#(\d+)')
	poll_content              = re.compile(r'<div>\s+(.+?)\s+</div>\s+<br>')
	poll_option               = re.compile(r'<label class="(.+?) ">\s+<input type="\1" name="reponse_\d*" id="reponse_(\d+)" value="\2" .+?/>\s+(.+?)\s+</label>')
	poll_percentage           = re.compile(r'reponse-sondage">.+?\((\d+)\)</div>')
	post                      = re.compile(r'<div id="m\d')
	private_message           = re.compile(r'<div id="m\d" (.+?</div>\s+</div>\s+</div>\s+</td>\s+</tr>)')
	private_message_data      = re.compile(r'<.+?id="message_(\d+)">(.+?)</div>\s+</div>\s+</div>\s+</td>\s+</tr>')
	profile_avatar            = re.compile(r'http://avatars\.atelier801\.com/\d+/\d+\.[a-zA-Z]+\?\d+')
	profile_birthday          = re.compile(r'Birthday :</span> ')
	profile_data              = re.compile(r'Messages: </span>(-?\d+).+?Prestige: </span>(\d+).+?Level: </span>(\d+)')
	profile_gender            = re.compile(r'Gender :.+? (\S+)\s+<br>')
	profile_id                = re.compile(r'profile\?pr=(.+?)"')
	profile_location          = re.compile(r'Location :</span> (.+?)  <br>')
	profile_presentation      = re.compile(r'cadre-presentation">\s*(.+?)\s*</div></div></div>')
	profile_soulmate          = re.compile(r'Soul mate :</span>.+?')
	profile_tribe             = re.compile(r'cadre-tribu-nom">(.+?)</span>.+?tr=(\d+)')
	recruitment               = re.compile(r'Recruitment : (.+?)<')
	search_list               = re.compile(r'<a href="(topic\?.+?)".+?>\s+(.+?)\s+</a></li>')
	secret_keys               = re.compile(r'<input type="hidden" name="(.+?)" value="(.+?)">')
	section_icon              = re.compile(r'sections/(.+?\.png)')
	section_topic             = re.compile(r'cadre-sujet-titre.+?href="topic\?.+?&t=(\d+).+?".+?>\s+([^>]+)\s+</a>')
	subsection                = re.compile(r'"cadre-section-titre-mini.+?(section.+?)".+?>\s+([^>]+)\s+</a>')
	title                     = re.compile(r'<title>(.+?)</title>')
	topic_div                 = re.compile(r'<div class="row">')
	total_entries             = re.compile(r'(\d+) entries')
	total_pages               = re.compile(r'"input-pagination".+?max="(\d+)"')
	tracker                   = re.compile(r'(.+?)</div>\s+</div>')
	tribe_list                = re.compile(r'<li class="nav-header">(.+?)</li>.+?\?tr=(\d+)"')
	tribe_log                 = re.compile(r'<td> (.+?) </td>')
	tribe_presentation        = re.compile(r'cadre-presentation"> (.+?) </div>')
	tribe_rank                = re.compile(r'<div class="rang-tribu"> (.+?) </div>')
	tribe_rank_id             = re.compile(r'<tr id="(\d+)"> <td>(.+?)</td>')
	tribe_rank_list           = re.compile(r'<h4>Ranks</h4>(.+?)</div>\s+</div>')
	tribe_section_id          = re.compile(r'"section\?f=(\d+)&s=(\d+)".+?/>\s*(.+?)\s*</a>')
