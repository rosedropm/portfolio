# Esther Jhang 作品集｜GitHub 發布與編輯說明

這個資料夾是可上傳 GitHub 的完整網站。包含網站內容、照片、Pages CMS 中文編輯欄位，以及 GitHub Pages 自動發布流程。

**本版本請使用 GitHub Actions 發布，不要選 Deploy from a branch。** 因為每次從後台修改文字或照片後，需要自動把內容轉成網頁。你不必在電腦安裝程式或手動執行建置。

## 1. 先在電腦看網站

解壓縮後，開啟資料夾內的 `index.html`。所有主要頁面、照片與樣式已一起打包，可離線瀏覽。作品的 Instagram／Facebook 連結需要網路。

根目錄的 HTML 是交付當下的預覽版本。後台更新後，正式網站會使用 GitHub 自動產生的新版本；這些預覽 HTML 不會回寫更新。後續請以正式網址查看最新內容。

## 2. 第一次發布到 GitHub

1. 登入 GitHub，建立新的 repository（儲存庫）。
2. 建議名稱填 `你的GitHub帳號.github.io`。例如帳號是 `esther-example`，名稱就是 `esther-example.github.io`。這裡是格式範例，不是已替你建立的帳號或網址。
3. 使用 GitHub Free 時選 **Public**。這代表上傳的網站、內容檔和圖片都公開可見。只上傳這個交付包，不要上傳完整 Notion 原始匯出或其他私人資料。
4. 在 repository 選 **Add file → Upload files**。上傳解壓縮後資料夾裡的「內容」，不要只上傳 ZIP，也不要把外層 `esther-portfolio` 資料夾整個套在 repository 外層。
5. 確認上傳後最外層能看見 `index.html`、`build.py`、`check.py`、`content`、`assets`、`.pages.yml` 及 `.github`。如果 Windows 沒顯示點號開頭的項目，開啟「檢視 → 顯示 → 隱藏的項目」。可以分批上傳資料夾。
6. 將變更儲存（Commit changes）到 **main** 分支。
7. 進入 **Settings → Pages → Build and deployment → Source**，選 **GitHub Actions**。不用新增 GitHub 顯示的範本，套件已包含完整流程。
8. 到 **Actions → Publish portfolio → Run workflow**，選 main 並執行。若第一次上傳時因 Pages 尚未啟用而失敗，完成第 7 步再重新執行即可。
9. 等到 build 和 deploy 都顯示綠色成功。回到 Settings → Pages，使用 GitHub 顯示的正式網址。

若使用一般名稱如 `portfolio`，也可以發布，網址通常會多一段 `/portfolio/`。網站連結與圖片已使用相對路徑，兩種 repository 命名都適用。正式網址與 `sitemap.xml` 會在發布時由 GitHub 自動產生，不需要先填帳號。

**如果 `.github` 沒有成功上傳：** 在 GitHub 點 Add file → Create new file，檔名完整輸入 `.github/workflows/deploy.yml`，貼上交付包內同名檔的內容並儲存。

**如果 `.pages.yml` 沒有成功上傳：** 以相同方式建立根目錄的 `.pages.yml` 並貼上內容。它必須保留這個檔名。內容使用 JSON 語法，這也是有效的 YAML 1.2 設定格式。

## 3. 啟用視覺化編輯後台

1. 開啟 [Pages CMS](https://app.pagescms.org/)，選擇用 GitHub 登入。
2. 依畫面安裝 Pages CMS 的 GitHub App，選擇擁有作品集 repository 的帳號。
3. 授權它存取這個作品集 repository。
4. 回到 Pages CMS，選擇 repository 與 **main** 分支。
5. 後台會讀取已附上的 `.pages.yml`，顯示中文內容項目。若要求你建立設定，先確認 `.pages.yml` 是否位於 repository 最外層、是否選到 main。

首次登入與 GitHub 授權需要由你本人完成。此交付包不含登入資訊，也尚未替你連接 Pages CMS 帳號。後台介面外框可能是英文，但網站欄位與操作提示已設為中文。

## 4. 後台每個項目可以改什麼

| 後台項目 | 可修改內容 |
| --- | --- |
| 基本資料・聯絡・履歷 | 姓名、職稱、Email、所在地、履歷檔、聯絡區標題 |
| 首頁與分類頁文字 | 首頁標題、介紹、主視覺、圖片說明、各列表頁簡介 |
| 關於我 | 個人照片、自介、工作經歷、核心能力與工具 |
| 專案案例 | 案例名稱、成果數字、策略、執行段落、圖片與分工 |
| 內容作品 | 文字文案、社群圖文、短影音作品與原始連結 |
| 攝影相簿 | 新增攝影系列、封面、照片及圖說 |

### 修改文字

選擇頁面 → 在欄位中修改 → 儲存。內文用空一行分段；不用輸入 HTML 或 Markdown。這是表單式內容編輯，不是拖拉整個網站版面的設計工具。

### 更換照片

在「封面圖片」「個人照片」或「作品圖片／相簿」欄位選取或上傳圖片，填寫圖片描述，再儲存。相簿每個項目都有圖片、描述與圖說，可新增、刪除與調整順序。

建議一般照片使用 JPG 或 WebP，長邊約 1600–2400 像素。長版網頁截圖可保留較高解析度。避免只把圖片傳進媒體庫卻沒有在內容欄位選取它；未引用的檔案不會出現在網站。

### 新增作品或相簿

1. 進入「專案案例」「內容作品」或「攝影相簿」，新增一筆內容。
2. 填「網址代稱」，例如 `summer-campaign`。只能使用小寫英文、數字和連字號，同一分類內不可重複。
3. 填列表名稱、大標題、作品簡介、角色與分類。
4. 上傳封面，新增文章段落及圖片。無封面時，內容作品可用「無圖片時的文字封面」呈現標題文字。
5. 設定排列順序（小數字在前），並開啟「顯示在網站上」。
6. 儲存後，新作品會自動出現在列表，並產生自己的頁面。

範例路徑：`works/summer-campaign/index.html`。發布後盡量不要修改網址代稱，因為舊連結不會自動轉址。

### 調整首頁精選

在專案或內容作品裡開啟「首頁精選」。首頁會依「排列順序」顯示前 3 筆已發布且勾選的項目。攝影區顯示前 3 組已發布相簿。

### 隱藏或刪除作品

關閉「顯示在網站上」可以從網站移除該作品。公開 repository 中的內容檔與 Git 紀錄仍可能可見，所以這個開關不適合存放機密草稿。

刪除圖片前，先從作品、封面和相簿中移除引用。若刪掉仍被引用的照片，檢查會阻止發布，原本成功發布的網站版本會繼續保留。

### 上傳履歷

進入「基本資料・聯絡・履歷」，在「履歷 PDF」上傳檔案。關於我頁會自動顯示下載按鈕。目前未附個人履歷 PDF，因此按鈕先隱藏。

## 5. 儲存後何時看得到

Pages CMS 儲存到 main → GitHub Actions 建置與檢查 → GitHub Pages 更新。通常需等待一小段時間，實際以 Actions 狀態為準。成功後重新整理正式網站；必要時使用 Ctrl+F5。

若網站沒變：先確認編輯的是 main，再看 Actions 最新一次是否成功。不要改選 Deploy from a branch，否則可能只顯示套件內舊的預覽 HTML。

Notion 不會自動同步到這個網站。後續請以 Pages CMS 的內容為主要發布版本；仍可在 Notion 草擬後貼入後台。

## 6. 已整理的內容與待補項目

- 3 個代表專案：授權師資招募、VDream 品牌落地、LINE OA 與客服流程。
- 6 組內容作品：品牌社群、獨立圖文、創辦人敘事、課程文案、商品內容與短影音企劃。
- 3 組攝影系列：Framtiden.29、Opus、皮膚管理店記錄。
- 關於我、網站地圖、404 頁、手機版選單、分類篩選、圖片放大與原圖入口。
- 保留原作品集的數字限制與協作分工。VDream 的 27 位是確認參與意願；不是已到場或已成交。
- 婦女節與課程文案目前收錄原作品標題、系列介紹及連結，沒有補寫成你的完整原文。你可在後台「文章段落」貼入全文。
- 短影音使用原平台連結，沒有下載影片或加入大量第三方嵌入；原平台可能要求登入。
- VDream 簡報沿用原作品集已模糊／去識別化的版本，沒有放入完整內部簡報。
- 43 張實際使用的圖片已存放在網站素材中，不依賴會過期的 Notion 圖片網址。履歷 PDF 尚待你上傳。

## 7. Sitemap

```text
首頁 index.html
├─ 專案案例 projects/index.html
│  ├─ instructor-recruitment/index.html
│  ├─ vdream-launch/index.html
│  └─ line-oa/index.html
├─ 內容作品 works/index.html
│  ├─ brand-social/index.html
│  ├─ social-visuals/index.html
│  ├─ founder-stories/index.html
│  ├─ course-copy/index.html
│  ├─ product-story/index.html
│  └─ short-video/index.html
├─ 攝影 photography/index.html
│  ├─ framtiden/index.html
│  ├─ opus/index.html
│  └─ skin-studio/index.html
├─ 關於我 about/index.html（含 #contact）
├─ 網站地圖 sitemap.html
└─ 404.html
```

`sitemap.xml` 與正式網址的 canonical 標記會在 GitHub 發布時產生。交付時尚無正式帳號／網域，因此離線預覽包不包含假網址的 sitemap.xml。

## 8. 給後續協助修改網站的人

內容在 `content/`，樣式在 `assets/style.css`，互動在 `assets/app.js`。`build.py` 是不依賴第三方套件的 Python 靜態產生器，將 JSON 內容轉成 HTML；`check.py` 檢查本地連結、圖片、標題與錨點。Pages CMS 使用 `.pages.yml`。

需要 Python 3.11 或更新版本。開發者可執行：

```text
python build.py
python check.py _site
python -m http.server 8000 --directory _site
```

開啟 `http://localhost:8000`。如果要測正式網域的 sitemap，設定環境變數 `SITE_URL`，或在後台填寫「網站正式網址」。一般 GitHub Pages 使用者可維持空白。

自動流程只發布產生後的 `_site`；不把後台設定、內容原始檔或建置腳本當作網站檔案部署。不過 Public repository 本身仍公開可讀。

## 9. 來源與驗證範圍

內容由 [Esther Jhang Portfolio](https://www.notion.so/2c2d8302497e802d9fe4c781afec75e5) 及其作品頁整理。網站簡介與標題有為閱讀動線改寫，成果數字依原作品集自述；圖片取自該作品集。

發布方式依 [GitHub Pages 自訂工作流程](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)，後台設定依 [Pages CMS 文件](https://pagescms.org/docs/configuration/content/) 與 [媒體設定](https://pagescms.org/docs/configuration/media/)。

已在本機進行靜態建置、頁面與圖片連結檢查，以及新增／修改／隱藏作品的資料建置測試。尚未在你的 GitHub 帳號執行實際發布，也未登入你的 Pages CMS 驗證授權流程；這兩項會在你完成首次設定後啟用。


## 10. 全站字型：GenKiMinJP

全站文字使用 emfont 提供的 GenKiMinJP Webfont，包含中文、英文姓名、導覽與按鈕。內文使用 400、標題與導覽使用 500、重點文字使用 600；成果數字保留較輕的展示字重。

每一頁會載入以下三個官方 CSS 網址：

- https://font.emtech.cc/css/GenKiMinJP/400
- https://font.emtech.cc/css/GenKiMinJP/500
- https://font.emtech.cc/css/GenKiMinJP/600

這次採外部 Webfont 載入，不把字型檔打包到 GitHub。首次使用需要網路；若字型未載入或缺少某個字元，會使用候補字型，網站仍能閱讀。離線預覽不保證顯示 GenKiMinJP。

文字與照片仍可用 Pages CMS 編輯。字型設定位於 build.py 的共用頁首與 assets/style.css，沒有新增後台字型切換欄位。

依 [emfont 快速入門](https://font.emtech.cc/docs/setup) 及 [指定字重載入方式](https://font.emtech.cc/docs/css) 設定。若已發布網站，更新 build.py、assets/style.css 後，GitHub Actions 會自動重新發布所有頁面；直接重新上傳最新版完整包也可以。
