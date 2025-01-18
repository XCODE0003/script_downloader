async function downloadFiles(linksText) {
    // Загружаем JSZip
    const JSZipScript = document.createElement('script');
    JSZipScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js';
    document.body.appendChild(JSZipScript);
    await new Promise(resolve => JSZipScript.onload = resolve);
    
    const zip = new JSZip();
    
    const links = linksText
        .split('\n')
        .map(link => link.trim())
        .filter(link => 
            link && 
            !link.includes('saveSettings.do') && 
            !link.includes('reloadBalance.do')
        );
    
    const uniqueLinks = [...new Set(links)];
    const totalFiles = uniqueLinks.length;
    
    const progressDiv = document.createElement('div');
    progressDiv.style.position = 'fixed';
    progressDiv.style.top = '10px';
    progressDiv.style.left = '10px';
    progressDiv.style.backgroundColor = 'white';
    progressDiv.style.padding = '10px';
    progressDiv.style.border = '1px solid black';
    progressDiv.style.zIndex = '9999';
    document.body.appendChild(progressDiv);

    async function downloadFile(url, index) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const blob = await response.blob();
            
            const urlPath = new URL(url).pathname;
            const filePath = urlPath.replace(/^\/api\/slots\//, '');
            
            zip.file(filePath, blob);
            
            const progress = Math.round((index + 1) / totalFiles * 100);
            progressDiv.innerHTML = `
                Загружено: ${index + 1} из ${totalFiles} файлов<br>
                Прогресс: ${progress}%<br>
                Текущий файл: ${filePath}
            `;
            
            return true;
        } catch (error) {
            console.error(`Ошибка при скачивании ${url}:`, error);
            return false;
        }
    }

    let successCount = 0;
    const startTime = Date.now();

    for (let i = 0; i < uniqueLinks.length; i++) {
        const success = await downloadFile(uniqueLinks[i], i);
        if (success) successCount++;
        
        const elapsed = Date.now() - startTime;
        const averageTimePerFile = elapsed / (i + 1);
        const remainingFiles = totalFiles - (i + 1);
        const estimatedRemainingTime = Math.round(remainingFiles * averageTimePerFile / 1000);
        
        progressDiv.innerHTML += `<br>Осталось примерно: ${estimatedRemainingTime} секунд`;
        
        await new Promise(resolve => setTimeout(resolve, 300));
    }

    progressDiv.innerHTML = 'Создание архива...';
    const content = await zip.generateAsync({type: 'blob'});
    
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(content);
    link.download = 'game_files.zip';
    link.click();
    window.URL.revokeObjectURL(link.href);

    const totalTime = Math.round((Date.now() - startTime) / 1000);
    progressDiv.innerHTML = `
        Загрузка завершена!<br>
        Успешно загружено: ${successCount} из ${totalFiles} файлов<br>
        Общее время: ${totalTime} секунд
    `;
    
    setTimeout(() => progressDiv.remove(), 5000);
}

const linksText = `
https://www.rijksmuseum.nl/statics/generated/focus-point-image.87784938e395bb8ebb12.mjs
https://www.rijksmuseum.nl/statics/generated/navigation.5f56ade719043353879d.mjs
https://www.rijksmuseum.nl/statics/generated/tooltip-toggle-content.433fc55fa09c525aff46.mjs
https://www.rijksmuseum.nl/statics/generated/accessibility-helper.905a44691b0e0c934aae.mjs
https://www.rijksmuseum.nl/statics/generated/height-expander.bfd0eb974f94c089d752.mjs
https://www.rijksmuseum.nl/statics/generated/article-selection.b24d9d7f1159e6ff340a.mjs
https://www.rijksmuseum.nl/statics/generated/wizard-steps.05df99f586c851b0df87.mjs
https://www.rijksmuseum.nl/statics/generated/shop-summary.15f8ffe5f4e919ad76cc.mjs
https://www.rijksmuseum.nl/statics/generated/vue-router.267c67868476d2d396f3.mjs


`;
downloadFiles(linksText);