//Console.log() is the same as System.out.println() or print() etc.
console.log("This is my JS Tutorial!");
var exampleVariable = 15;
console.log("The Variable's Value Is: " + exampleVariable);

//Use the Alert function to have a message box pop up: This might only work as a script on a webpage
alert("This is an example of what the alert function does!"); 
//This command pulls an element by its ID and modifies it
document.getElementById("SF_V_Seattle").innerText = "Seattle V.S. San Francisco: My first wrong guess, I was correct about SF winning but Seattle didn't cover the spread.";
document.getElementById("LA_V_Jacksonville").innerText = "Jacksonville V.S. Los Angelos: Holy shit, I correctly predicted this game and the spread, but I did not expect it to go the way it did.";
document.getElementById("sampleHeader").innerText = exampleVariable + " is the value of this variable!";
//The examples above use the .innerText command, however, .innerHTML will modify the HTML Structure itself.
myElement = document.getElementById("testingParagraph");
myElement.innerHTML = "<strong>You can change html structure in this example we change the p element to the strong element!</strong>";
