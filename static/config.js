/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	// code snippet restricts languages to JavaScript and PHP.
	config.toolbar = [
		{ name: 'tools', items: [ 'Maximize' ] },
		{ name: 'clipboard', items: [ 'Undo', 'Redo' ] },
		{ name: 'clipboard', items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'  ] },
		{ name: 'editing', items: [ 'SelectAll', '-','Find', 'Replace', '-',  'Scayt', 'AutoCorrect' ] },
		{ name: 'links', items: [ 'Link', 'Unlink', 'Anchor' ] },
		{ name: 'bidi', items: [ 'BidiLtr', 'BidiRtl' ] },
		{ name: 'insert', items: [ 'CodeSnippet', 'Image', 'Table', 'Smiley', 'SpecialChar' ] },
		{ name: 'insert', items: [ 'HorizontalRule', 'PageBreak' ] },
		{ name: 'insert', items: [ 'Blockquote', 'CreateDiv' ] },
		{ name: 'colors', items: [ 'TextColor', 'BGColor' ] },
		{ name: 'basicstyles', items: [ 'Bold', 'Italic', 'Underline' ] },
		{ name: 'basicstyles', items: [ 'Strike', 'Subscript', 'Superscript' ] },
		{ name: 'basicstyles', items: [ 'CopyFormatting', 'RemoveFormat' ] },
		{ name: 'paragraph', items: [ 'NumberedList', 'BulletedList' ] },
		{ name: 'paragraph', items: [ 'Outdent', 'Indent' ] },
		{ name: 'paragraph', items: [ 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-' ] },
		{ name: 'styles', items: [ 'Styles', 'Format', 'Font', 'FontSize' ] },
	];
};