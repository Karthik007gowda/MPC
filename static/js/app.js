document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('mpc-file-input');
    const fileInfo = document.getElementById('file-info');
    const fileNameSpan = document.getElementById('file-name');
    const executeBtn = document.getElementById('execute-btn');
    const loadingSpinner = document.getElementById('loading-spinner');
    const outputZone = document.getElementById('output-zone');
    const downloadBtn = document.getElementById('download-btn');
    const issuesCount = document.getElementById('issues-count');

    let selectedFile = null;

    // Trigger File Input Click
    dropZone.addEventListener('click', () => fileInput.click());

    // File Selected
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag and Drop Effects
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('bg-dark');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('bg-dark');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('bg-dark');
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    function handleFile(file) {
        selectedFile = file;
        fileNameSpan.textContent = file.name;
        fileInfo.classList.remove('d-none');
        executeBtn.classList.remove('disabled');
        outputZone.classList.add('d-none');
    }

    // Execute Transcompilation
    executeBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('mpc_file', selectedFile);

        executeBtn.classList.add('disabled');
        loadingSpinner.classList.remove('d-none');
        outputZone.classList.add('d-none');

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            loadingSpinner.classList.add('d-none');

            if (response.ok && data.status === 'SUCCESS') {
                downloadBtn.href = data.download_url;
                issuesCount.textContent = data.issue_count;
                outputZone.classList.remove('d-none');
            } else {
                alert('Error: ' + (data.error || 'Conversion failed.'));
                executeBtn.classList.remove('disabled');
            }
        } catch (error) {
            loadingSpinner.classList.add('d-none');
            executeBtn.classList.remove('disabled');
            alert('Server Communication Error: ' + error.message);
        }
    });
});
