        $(document).ready(function(){

            var counterIngredient = 2;

            $("#addIngredientButton").click(function () {
	            var newTextBoxIngredientDiv = $(document.createElement('div')).attr("id", 'TextBoxIngredientDiv' + counterIngredient);
    	        newTextBoxIngredientDiv.after().html(
                '<label>Ingredient #'+ counterIngredient + ' : </label>' + '<input type="text" name="ingredient' + counterIngredient + '" id="ingredient' + counterIngredient + '" value="" >'+
                '<label> Amount : </label>' + '<input type="text" name="textbox amount' + counterIngredient + '" id="amount' + counterIngredient + '" value="" >' + 
                '<label> Unit : </label>' +  '<input type="text" name="textbox unit' + counterIngredient + '" id="unit' + counterIngredient + '" value="" >');
	            newTextBoxIngredientDiv.appendTo("#TextBoxesIngredientGroup");
    	        counterIngredient++;
            });

            $("#removeIngredientButton").click(function () {
	            if(counterIngredient==1){
                    alert("No more ingredients to remove");
                    return false;
                }
	            counterIngredient--;
                $("#TextBoxIngredientDiv" + counterIngredient).remove();
            });


            var counterInstruction = 2;
            $("#addInstructionButton").click(function () {
                var newTextBoxDiv = $(document.createElement('div')).attr("id", 'TextBoxDivInstruction' + counterInstruction);
    	        newTextBoxDiv.after().html(
                '<label>Step #'+ counterInstruction + ' : </label>' + '<input type="text" name="textbox_step' + counterInstruction + '" id="step' + counterInstruction + '" value="" >');
    	        newTextBoxDiv.appendTo("#TextBoxesGroupInstruction");
    	        counterInstruction++;
             });

            $("#removeInstructionButton").click(function () {
	            if(counterInstruction==1){
                    alert("No more steps to remove");
                    return false;
                }
	            counterInstruction--;

                $("#TextBoxDivInstruction" + counterInstruction).remove();
            });


            $("#submitRecipe").click(function () {
        	    var msg = '';
                for(i=1; i<counterIngredient; i++) {
                    msg += "\n Ingredient #" + i + " : " + $('#ingredient' + i).val();
                    msg += " : " + $('#amount' + i).val();
                    msg += "" + $('#unit' + i).val();
                }
        	    for(i=1; i<counterInstruction; i++){
                    msg += "\n Step #" + i + " : " + $('#step' + i).val();
    	        }

            alert(msg);
            });
        });
