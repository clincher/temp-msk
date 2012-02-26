
    window.onload = function()
    {
        // create the FCK Editor and replace the specific text area with it        
		var eid = ['id_content', 'id_description', 'id_smallcontent', "id_property"];
		for(i=0;i<eid.length;i++){
			if(document.getElementById(eid[i])){  
				var element = $('label[for=' + eid[i] + ']')[0];
				$(element).css("display","block");
				$(element).css("clear","both");
				$(element).css("width","100%");
				$(element).css("height","18px");

//				var contentElement = new Element('div id="contentElement"', {id: 'contentElement'});
				$(element).insertAfter('<div id="contentElement"></div>');
				$('#contentElement').css("display","block");
				$('#contentElement').css("clear","both");
				$('#contentElement').css("width","100%");
				$('#contentElement').css("height","3px");

				var CKeditor = new CKEDITOR.replace(eid[i], { 
					customConfig : '', 
					language : 'ru', 
					filebrowserBrowseUrl: '/admin/filemanager/popup/',
					filebrowserImageBrowseUrl : '/admin/filemanager/popup/?type=Images',
					filebrowserUploadUrl : '/admin/filemanager/popup/',
					filebrowserImageUploadUrl : '/admin/filemanager/popup/?type=Images'

				});



				CKeditor.BasePath = "/media/ckeditor/";
	        }
		}
    }

