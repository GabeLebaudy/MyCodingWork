//Console.log() is the same as System.out.println() or print() etc.
console.log("This is my JS Tutorial!");
var exampleVariable = 15;
console.log("The Variable's Value Is: " + exampleVariable);

//Use the Alert function to have a message box pop up: This might only work as a script on a webpage
alert("This is an example of what the alert function does!"); 
//This command pulls an element by its ID and modifies it
document.getElementById("SF_V_Seattle").innerText = "Seattle V.S. San Francisco: My first wrong guess, I was correct about SF winning but Seattle didn't cover the spread.";
document.getElementById("LA_V_Jacksonville").innerText = "Jacksonville V.S. Los Angelos: Holy shit, I correctly predicted this game and the spread, but I did not expect it to go the way it did.";
document.getElementById("Miami_V_Buffalo").innerText = "Miami V.S. Buffalo: Honestly did not expect this game to go the way it did, I thought the dolphins would not be able to get anything going, which was mostly true, however Josh Allen was nearly responsible for all points scored in the game.";
document.getElementById("NewYork_V_Minnesota").innerText = "New York V.S. Minnesota: I thought the score would be lower, but I was right on the money for this game, Giants win and cover the spread.";
document.getElementById("Baltimore_V_Cincinatti").innerText = "Baltimore V.S. Cincinnati: Game was much closer than I expected with Tyler Huntly at the QB spot. Ravens could be dangerous next year if Lamar chooses to stay.";
document.getElementById("sampleHeader").innerText = exampleVariable + " is the value of this variable!";
//The examples above use the .innerText command, however, .innerHTML will modify the HTML Structure itself.
myElement = document.getElementById("testingParagraph");
myElement.innerHTML = "<strong>You can change html structure in this example we change the p element to the strong element!</strong>";
