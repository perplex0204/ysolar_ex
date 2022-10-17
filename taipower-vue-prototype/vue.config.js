const path = require('path');

function resolve (dir) { return path.join(__dirname, dir) }

module.exports = {
    publicPath:'./',
    configureWebpack: {
      devtool: 'source-map',
      module: {
        rules: [
          {
            test: /\.mjs$/,
            include: /node_modules/,
            type: "javascript/auto"
          }
        ] 
      }
    },
    chainWebpack: (config)=>{ 
      config.resolve.alias 
      .set('@', resolve('src')) 
      .set('assets',resolve('src/assets')) 
      .set('components',resolve('src/components')) 
      // Set Page Title and favicon to corresponding pageType
      config.plugin('define').tap(args => {
        let pageType = ""
        if("VUE_APP_PAGETYPE" in args[0]['process.env']){
          pageType = 'paets'
        }
        pageType = pageType.substring(1, pageType.length-1)
        config.plugin('html').tap(_args =>{
          let title = `${require("./src/lang/locale/zh_tw.json").title[pageType]}`
          _args[0].title = title
          //config favicon
          _args[0].favicon = 'public/favicon.ico' 
          const fs = require('fs')
          if(pageType.length > 0 && fs.existsSync(`./public/imgs/${pageType}/favicon.ico`)){
            _args[0].favicon = `./public/imgs/${pageType}/favicon.ico`
          }else if(pageType.length > 0){
            console.log(`favicon not found at ./public/imgs/${pageType}/favicon.ico`)
          }
          return _args;
        })
        return args
      })
    }

}