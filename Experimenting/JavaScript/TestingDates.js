const currentDate = new Date();
let currentYear = currentDate.getFullYear();
let currentMonthInt = currentDate.getMonth();
function getDayName(dateStr, locale)
{
    let date = new Date(dateStr);
    return date.toLocaleDateString(locale, { weekday: 'long' });        
}
currentMonthInt++;
let monthNumString = currentMonthInt.toString();
let yearNumString = currentYear.toString();
let dateFormat = monthNumString + '/' + '1' + '/' + yearNumString;
let day = getDayName(dateFormat, "en-US");
console.log(day);