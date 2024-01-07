console.log("Hello from script.js")

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function reset_db() {
    $.get('/reset_db', function(response) {
        console.log("db_reset...");
        alert(response);
        sleep(1000);
        location.reload();
    });
}