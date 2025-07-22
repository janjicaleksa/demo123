// File upload handling
async function uploadFiles(clientName, files) {
    const formData = new FormData();
    formData.append('client_name', clientName);
    
    for (const file of files) {
        formData.append('files', file);
    }
    
    try {
        const response = await fetch('/api/upload/', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Upload error:', error);
        throw error;
    }
}

// Extract tables from uploaded files
async function extractTables(clientName) {
    try {
        const response = await fetch(`/api/extract/?client_name=${encodeURIComponent(clientName)}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error(`Extraction failed: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Extraction error:', error);
        throw error;
    }
}

// Generate unified report
async function generateReport(clientName) {
    try {
        const response = await fetch(`/api/generate-report/?client_name=${encodeURIComponent(clientName)}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error(`Report generation failed: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Report generation error:', error);
        throw error;
    }
}

// Fetch results for a client
async function getResults(clientName) {
    try {
        const response = await fetch(`/api/results/${encodeURIComponent(clientName)}`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch results: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Results fetch error:', error);
        throw error;
    }
}

// Download report as Excel
function downloadExcel(data, filename) {
    // Implementation will depend on the Excel generation library used
    // This is a placeholder for the download functionality
    console.log('Downloading Excel:', filename, data);
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('sr-RS', {
        style: 'currency',
        currency: 'RSD'
    }).format(amount);
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
        setTimeout(() => {
            errorDiv.classList.add('hidden');
        }, 5000);
    }
}

// Show success message
function showSuccess(message) {
    const successDiv = document.getElementById('success-message');
    if (successDiv) {
        successDiv.textContent = message;
        successDiv.classList.remove('hidden');
        setTimeout(() => {
            successDiv.classList.add('hidden');
        }, 5000);
    }
} 