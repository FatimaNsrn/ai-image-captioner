document.getElementById('imageInput').addEventListener('change', function(event) {
  const file = event.target.files[0];
  const preview = document.getElementById('preview');
  const captionText = document.getElementById('captionText');

  // Clear previous caption when a new image is selected
  captionText.textContent = 'No caption generated yet.';

  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      preview.src = e.target.result;
      preview.style.display = 'block';
    }
    reader.readAsDataURL(file);
  } else {
    preview.src = '';
    preview.style.display = 'none';
  }
});


document.getElementById('uploadButton').addEventListener('click', () => {
  const fileInput = document.getElementById('imageInput');
  const file = fileInput.files[0];
  const captionText = document.getElementById('captionText');

  if (!file) {
    alert('Please choose an image first.');
    return;
  }

  const formData = new FormData();
  formData.append('image', file);

  captionText.textContent = 'Generating caption...';

  fetch('/generate_caption', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.caption) {
        captionText.textContent = data.caption;
      } else {
        captionText.textContent = 'Failed to generate caption.';
      }
    })
    .catch(error => {
      console.error('Error:', error);
      captionText.textContent = 'Error occurred while generating caption.';
    });
});
