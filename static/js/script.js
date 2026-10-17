/**
 * ResumeScreen AI - Client-side JavaScript
 */

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB
const ALLOWED_EXTENSIONS = ['pdf', 'docx'];

function initUploadPage() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('resumeInput');
    const browseBtn = document.getElementById('browseBtn');
    const removeBtn = document.getElementById('removeFile');
    const submitBtn = document.getElementById('submitBtn');
    const filePreview = document.getElementById('filePreview');
    const dropZoneContent = dropZone.querySelector('.drop-zone-content');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const uploadForm = document.getElementById('uploadForm');

    if (!dropZone) return;

    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    dropZone.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover'].forEach(event => {
        dropZone.addEventListener(event, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(event => {
        dropZone.addEventListener(event, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('drag-over');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileSelect(fileInput.files[0]);
        }
    });

    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetFileInput();
    });

    uploadForm.addEventListener('submit', (e) => {
        if (!fileInput.files.length) {
            e.preventDefault();
            alert('Please select a resume file to upload.');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing...';
    });

    function handleFileSelect(file) {
        const extension = file.name.split('.').pop().toLowerCase();

        if (!ALLOWED_EXTENSIONS.includes(extension)) {
            alert('Invalid file type. Only PDF and DOCX files are allowed.');
            resetFileInput();
            return;
        }

        if (file.size > MAX_FILE_SIZE) {
            alert('File is too large. Maximum allowed size is 5 MB.');
            resetFileInput();
            return;
        }

        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        dropZoneContent.classList.add('d-none');
        filePreview.classList.remove('d-none');
        submitBtn.disabled = false;
    }

    function resetFileInput() {
        fileInput.value = '';
        dropZoneContent.classList.remove('d-none');
        filePreview.classList.add('d-none');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="bi bi-search me-2"></i>Analyze Resume';
    }

    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    }
}

function initDashboardCharts(categoryData, trendData) {
    const pieCanvas = document.getElementById('pieChart');
    const barCanvas = document.getElementById('barChart');

    if (!pieCanvas || !barCanvas) return;

    const colors = [
        '#6366f1', '#8b5cf6', '#0ea5e9', '#10b981', '#f59e0b',
        '#ef4444', '#06b6d4', '#ec4899', '#84cc16', '#f97316',
        '#a855f7', '#14b8a6', '#e11d48', '#7c3aed', '#0891b2',
        '#65a30d', '#dc2626', '#2563eb', '#9333ea', '#059669',
        '#d97706', '#be185d', '#4f46e5', '#0d9488', '#ca8a04'
    ];

    if (categoryData && categoryData.length > 0) {
        new Chart(pieCanvas, {
            type: 'doughnut',
            data: {
                labels: categoryData.map(d => d.prediction),
                datasets: [{
                    data: categoryData.map(d => d.count),
                    backgroundColor: colors.slice(0, categoryData.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            font: { family: 'Poppins', size: 11 },
                            padding: 12
                        }
                    }
                }
            }
        });
    } else {
        pieCanvas.parentElement.innerHTML = '<p class="text-muted text-center py-5">No category data available yet.</p>';
    }

    if (trendData && trendData.length > 0) {
        new Chart(barCanvas, {
            type: 'bar',
            data: {
                labels: trendData.map(d => d.upload_date),
                datasets: [{
                    label: 'Uploads',
                    data: trendData.map(d => d.count),
                    backgroundColor: 'rgba(99, 102, 241, 0.7)',
                    borderColor: '#6366f1',
                    borderWidth: 1,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1, font: { family: 'Poppins' } }
                    },
                    x: {
                        ticks: { font: { family: 'Poppins', size: 11 } }
                    }
                }
            }
        });
    } else {
        barCanvas.parentElement.innerHTML = '<p class="text-muted text-center py-5">No upload trend data available yet.</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.glass-nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
            } else {
                navbar.style.boxShadow = 'none';
            }
        });
    }

    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            link.style.color = '#6366f1';
        }
    });
});
