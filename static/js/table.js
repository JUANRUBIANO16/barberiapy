$(document).ready(function(){

	// activar tooltips
	$('[data-toggle="tooltip"]').tooltip();

	// seleccionar todos los checkboxes
	var checkbox = $('table tbody input[type="checkbox"]');

	$("#selectAll").click(function(){

		if(this.checked){
			checkbox.each(function(){
				this.checked = true;
			});
		}else{
			checkbox.each(function(){
				this.checked = false;
			});
		}

	});

	checkbox.click(function(){

		if(!this.checked){
			$("#selectAll").prop("checked", false);
		}

	});

});