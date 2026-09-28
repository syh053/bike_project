import { createPinia } from 'pinia'

// 匯出共用的 pinia instance,讓動態掛載的元件(如地圖 popup)也能存取同一份 store 狀態
export const pinia = createPinia()
