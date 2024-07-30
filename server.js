const express = require('express')
const exphbs = require('express-handlebars')

const app = express()

app.use(express.static(__dirname + "/public"))

app.engine("hbs", exphbs.engine({defaultLayout: 'main', extname:'hbs'}))
app.set("view engine", "hbs")
app.set('views', './views')

app.get("/", (req, res) => {
     res.render("home", {title: "Group5"})
})

app.listen(3000)