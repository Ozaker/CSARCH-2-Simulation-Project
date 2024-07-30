const express = require('express')
const exphbs = require('express-handlebars')

const app = express()

app.use(express.static(__dirname + "/public"))

app.engine("hbs", exphbs.engine({extname:'hbs'}))
app.set("view engine", "hbs")
app.set('views', './views')

app.get("/", (req, res) => {
     console.log("here")
     res.render("home")
})

app.listen(3000)