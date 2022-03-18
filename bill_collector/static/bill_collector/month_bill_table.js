const month_bill_tb_path = window.location.pathname;


function getMonthAndYearOfPage() {
    const pathArray = month_bill_tb_path.split("/");
    const month = pathArray[pathArray.length-2];
    const year = pathArray[pathArray.length-3];
    return [month, year];
}

function appendMonthAndYear(path) {
    var [month, year] = getMonthAndYearOfPage();
    if (path[path.length-1] == "/") {
        return path + year + "/" + month + "/"
    } else {
        return path + "/" + year + "/" + month + "/"
    }
}

function getFirstDayOfMonth() {
    var [month, year] = getMonthAndYearOfPage();
    if (month.length == 1) {
        month = "0" + month;
    }
    return year+"-"+month+"-01";
}

function getDaysInMonth(year, month) {
    return new Date(year, month, 0).getDate();
}

function getLastDayOfMonth(){
    var [month, year] = getMonthAndYearOfPage();
    if (month.length == 1) {
        month = "0" + month;
    }
    var day = getDaysInMonth(year, month);
    day = day.toString();
    if (day.length == 1) {
        day = "0" + day;
    }
    return year+"-"+month+"-"+day;
}