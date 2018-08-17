        $(document).ready(function(){

            var counterIngredient = 2;

            $("#addIngredientButton").click(function () {
	            var newTextBoxIngredientDiv = $(document.createElement('div')).attr("id", 'TextBoxIngredientDiv' + counterIngredient);
    	        newTextBoxIngredientDiv.after().html(
                '<label>Ingredient #'+ counterIngredient + ' : </label>' + '<input type="text" name="ingredient' + counterIngredient + '" id="ingredient' + counterIngredient + '" value="" >'+
                '<label> Amount : </label>' + '<input type="textbox" name="amount' + counterIngredient + '" id="amount' + counterIngredient + '" value="" >' +
                '<label> Unit : </label>' +  '<input type="textbox" name="unit' + counterIngredient + '" id="unit' + counterIngredient + '" value="" >');
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
                '<label>Step #'+ counterInstruction + ' : </label>' + '<input type="text" name="step' + counterInstruction + '" id="step' + counterInstruction + '" value="" >');
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


            // $("#submitRecipe").click(function () {
            //   //creates a msg (string)
        	  //   var msg = '';
            //     for(i=1; i<counterIngredient; i++) {
            //         msg += "\n Ingredient #" + i + " : " + $('#ingredient' + i).val();
            //         msg += " : " + $('#amount' + i).val();
            //         msg += "" + $('#unit' + i).val();
            //     }
        	  //   for(i=1; i<counterInstruction; i++){
            //         msg += "\n Step #" + i + " : " + $('#step' + i).val();
    	      //   }
            //   //display the message
            //   var XHR = new XMLHttpRequest();
            //   var urlEncodedData = "";
            //   var urlEncodedDataPairs = [];
            //   var name;
            //
            //
            //   alert(msg);
            // });
           });

             function sendData() {
               var XHR = new XMLHttpRequest();
               // Bind the FormData object and the form element
               var FD = new FormData(newRecipe);

               // Define what happens on successful data submission
               XHR.addEventListener("load", function(event) {
                 alert(event.target.responseText);
               });
               // Define what happens in case of error
               XHR.addEventListener("error", function(event) {
                 alert('Oops! Something went wrong.');
               });
               // Set up our request
               XHR.open("POST", "/add_recipe");

               // The data sent is what the user provided in the form
               XHR.send(FD);
             }
