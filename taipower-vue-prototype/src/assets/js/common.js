import Plotly from "plotly.js-dist-min";

export default {
    round(num, n) {
        if (
            num == null ||
            num == "---" ||
            num == undefined ||
            num == "undefined"
        ) {
            return "---"
        } else {
            if (num > 0) {
            num = parseInt(num * Math.pow(10, n) + 0.5, 10) / Math.pow(10, n)
            } else if (num < 0) {
            num = num * -1
            num = (parseInt(num * Math.pow(10, n) + 0.5, 10) / Math.pow(10, n)) * -1
            }
            return num
        }
    },
    plot_resize(){
        let update = {
            width: "",
            heigth: "",
        }
        try{
            update = {
                width: document.getElementById('plot_div').clientWidth,
                height:  document.getElementById('plot_div').clientHeight,
                margin: {
                    l: 70,
                    r: 50,
                    b: 50,
                    t: 50,
                    pad: 20,
                }
            }
            if(document.getElementById('plot_div').clientWidth < 550){
                update.margin.l = 40
                update.margin.r = 40
                update.margin.pad = 1
            }
            Plotly.relayout("plot_div", update)
        }
        catch{
            return false
        }
        this.plot_text_color_fix(document.getElementById('plot_div'))
    },
    plot_resize_ref(plot_obj){
        let update = {
            width: "",
            heigth: "",
        }
        try{
            update = {
                width: plot_obj.clientWidth,
                height:  plot_obj.clientHeight,
                margin: {
                    l: 70,
                    r: 50,
                    b: 50,
                    t: 50,
                    pad: 20,
                }
            }
            if(plot_obj.clientWidth < 550){
                update.margin.l = 40
                update.margin.r = 40
                update.margin.pad = 1
            }
            Plotly.relayout(plot_obj, update)
        }
        catch{
            return false
        }
    },
    plot_margin(){
        let margin =  {
            l: 70,
            r: 50,
            b: 50,
            t: 50,
            pad: 20,
        }
        if(document.getElementById('plot_div').clientWidth < 550){
            margin.l = 40
            margin.r = 40
            margin.pad = 1
        }
        return margin
    },
    plot_margin_ref(plot_obj){
        let margin =  {
            l: 70,
            r: 50,
            b: 50,
            t: 50,
            pad: 20,
        }
        if(plot_obj.clientWidth < 550){
            margin.l = 40
            margin.r = 40
            margin.pad = 1
        }
        return margin
    },
    // Fix Plot Color to fit dark light mode
    plot_text_color_fix(plot_obj){
        if(plot_obj.querySelector('.g-gtitle text')){
            plot_obj.querySelector('.g-gtitle text').style.fill = "var(--bs-body-color)"
        }
        if(plot_obj.querySelector('.g-xtitle text')){
            plot_obj.querySelector('.g-xtitle text').style.fill = "var(--bs-body-color)"
        }
        if(plot_obj.querySelector('.g-ytitle text')){
            plot_obj.querySelector('.g-ytitle text').style.fill = "var(--bs-body-color)"
        }
        // trace
        plot_obj.querySelectorAll('.traces text').forEach(node=>{
            node.style.fill = "var(--bs-body-color)"
        })
        //tick
        plot_obj.querySelectorAll('.xtick text').forEach(node=>{
            node.style.fill = "var(--bs-body-color)"
        })
        plot_obj.querySelectorAll('.ytick text').forEach(node=>{
            node.style.fill = "var(--bs-body-color)"
        })
        //pie chart slice
        plot_obj.querySelectorAll('.slice .slicetext').forEach(node=>{
            node.style.fill = "var(--bs-body-color)"
        })
        plot_obj.querySelectorAll('.slice .textline').forEach(node=>{
            node.style.stroke = "var(--bs-body-color)"
        })
    },
    getCookie(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i <ca.length; i++) {
          let c = ca[i];
          while (c.charAt(0) == ' ') {
            c = c.substring(1);
          }
          if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
          }
        }
        return "";
    },
    formatDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();
    
        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;
    
        return [year, month, day].join('-');
    },
    //Split number with commas
    numberWithCommas(x) {
        if(!isNaN(parseFloat(x)) && !isNaN(x - 0))
            return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
        else
            return x
    }
}