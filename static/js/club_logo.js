function club_logo(){


fetch('/player_card/'+ID)
.then(function(response){
  return response.json()
}).then(function(data_input){

var data = data_input;

console.log(data)

document.getElementById('name').innerHTML = "Name: " + data[0].Name;
document.getElementById('age').innerHTML = "Age: " + data[0].Age;
document.getElementById('nationality').innerHTML = "Nationality: " + data[0].Nationality;
document.getElementById('club').innerHTML = "Club: " + data[0].Club;
document.getElementById('overall').innerHTML = "Overall: " + data[0].Overall;
document.getElementById('player_image').src = "https://futhead.cursecdn.com/static/img/20/players/"+ID+".png";


});


}