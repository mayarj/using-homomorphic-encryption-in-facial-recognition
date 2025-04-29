const form = document.getElementById('imageUploadForm');
const loadingMessage = document.getElementById('loadingMessage');

const updateImagePreview = (event) => {
    const file = event.target.files[0];
    if (file) {
        document.getElementById('imagePreview').src = URL.createObjectURL(file);
    }
};

form.addEventListener('change', function(event) {
    updateImagePreview(event);
});

form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(form);
    
    loadingMessage.style.display = 'block';
    
    fetch('api/process-image/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        loadingMessage.style.display = 'none';
        if (data.image) {
            document.getElementById('imagePreview').src = data.image;
        }
    })
    .catch(error => {
        loadingMessage.style.display = 'none';
        console.error('Error:', error);
    });
});

