//lang.js
import { createI18n } from 'vue-i18n/index'

import zh_tw from './locale/zh_tw.json'
import en_us from './locale/en_us.json'


const i18n = new createI18n({
    locale: 'zh-TW',
    fallbackLocale: 'zh-TW',   // 若選擇的語言缺少翻譯則退回的語言,
    silentTranslationWarn: true,
    messages:{
        'zh-TW': zh_tw,
        'en-US': en_us,
        'zh': zh_tw,
        'en': en_us,
    }
})

export default i18n
