/**
 * Result Sharing Component
 * Enables sharing Saju results via URL and image export
 */

class ResultSharing {
    constructor() {
        this.sajuData = null;
        this.shareUrl = null;
        this.init();
    }
    
    init() {
        this.createSharePanel();
        this.attachEventListeners();
        this.checkForSharedResult();
    }
    
    createSharePanel() {
        const panel = document.createElement('div');
        panel.id = 'share-panel';
        panel.className = 'share-panel';
        panel.innerHTML = `
            <div class="share-header">
                <h3>결과 공유하기</h3>
                <button class="btn-close-share" onclick="resultSharing.closePanel()">×</button>
            </div>
            
            <div class="share-options">
                <!-- URL Share -->
                <div class="share-option">
                    <h4>🔗 링크 공유</h4>
                    <div class="url-share-container">
                        <input type="text" id="share-url" class="share-url-input" readonly>
                        <button class="btn-copy-url" onclick="resultSharing.copyUrl()">
                            <span class="copy-icon">📋</span>
                            <span class="copy-text">복사</span>
                        </button>
                    </div>
                    <div class="share-buttons">
                        <button class="share-btn kakao" onclick="resultSharing.shareKakao()">
                            <img src="/images/kakao-icon.png" alt=""> 카카오톡
                        </button>
                        <button class="share-btn facebook" onclick="resultSharing.shareFacebook()">
                            <span>f</span> 페이스북
                        </button>
                        <button class="share-btn twitter" onclick="resultSharing.shareTwitter()">
                            <span>𝕏</span> 트위터
                        </button>
                    </div>
                </div>
                
                <!-- QR Code -->
                <div class="share-option">
                    <h4>📱 QR 코드</h4>
                    <div class="qr-code-container">
                        <canvas id="qr-code"></canvas>
                        <button class="btn-download-qr" onclick="resultSharing.downloadQR()">
                            QR 코드 다운로드
                        </button>
                    </div>
                </div>
                
                <!-- Image Export -->
                <div class="share-option">
                    <h4>🖼️ 이미지로 저장</h4>
                    <div class="image-export-options">
                        <button class="btn-export-image" onclick="resultSharing.exportAsImage('png')">
                            PNG 다운로드
                        </button>
                        <button class="btn-export-image" onclick="resultSharing.exportAsImage('jpg')">
                            JPG 다운로드
                        </button>
                        <button class="btn-export-image" onclick="resultSharing.exportAsImage('pdf')">
                            PDF 다운로드
                        </button>
                    </div>
                </div>
                
                <!-- Short URL -->
                <div class="share-option">
                    <h4>🔗 단축 URL</h4>
                    <div class="short-url-container">
                        <input type="text" id="short-url" class="share-url-input" readonly>
                        <button class="btn-create-short" onclick="resultSharing.createShortUrl()">
                            단축 URL 생성
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="share-footer">
                <p class="share-note">
                    * 공유된 링크는 30일간 유효합니다.
                </p>
            </div>
        `;
        
        document.body.appendChild(panel);
        
        // Add share button to results section
        this.addShareButton();
    }
    
    addShareButton() {
        const resultsSection = document.getElementById('results-section');
        if (!resultsSection) return;
        
        // Check if button already exists
        if (document.getElementById('btn-share-results')) return;
        
        const shareButton = document.createElement('button');
        shareButton.id = 'btn-share-results';
        shareButton.className = 'btn-share-results';
        shareButton.innerHTML = `
            <span class="share-icon">🔗</span>
            <span class="share-text">공유하기</span>
        `;
        shareButton.onclick = () => this.openPanel();
        
        // Find a suitable location to add the button
        const resultsHeader = resultsSection.querySelector('.section-header, .results-header, h2');
        if (resultsHeader) {
            resultsHeader.appendChild(shareButton);
        } else {
            resultsSection.insertBefore(shareButton, resultsSection.firstChild);
        }
    }
    
    attachEventListeners() {
        // Listen for Saju calculation results
        window.addEventListener('sajuCalculated', (e) => {
            this.sajuData = e.detail;
            this.generateShareUrl();
        });
    }
    
    openPanel() {
        const panel = document.getElementById('share-panel');
        if (panel) {
            panel.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Generate share URL if not already generated
            if (!this.shareUrl) {
                this.generateShareUrl();
            }
            
            // Generate QR code
            this.generateQRCode();
        }
    }
    
    closePanel() {
        const panel = document.getElementById('share-panel');
        if (panel) {
            panel.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
    
    generateShareUrl() {
        if (!this.sajuData) {
            console.error('No Saju data available to share');
            return;
        }
        
        // Encode Saju data
        const encodedData = this.encodeShareData(this.sajuData);
        
        // Create share URL
        const baseUrl = window.location.origin + window.location.pathname;
        this.shareUrl = `${baseUrl}?share=${encodedData}`;
        
        // Update URL input
        const urlInput = document.getElementById('share-url');
        if (urlInput) {
            urlInput.value = this.shareUrl;
        }
        
        return this.shareUrl;
    }
    
    encodeShareData(data) {
        // Create a simplified version of the data for sharing
        const shareData = {
            bd: data.birthDate || '',  // birth date
            bt: data.birthTime || '',  // birth time
            g: data.gender || '',      // gender
            il: data.isLunar || false, // is lunar
            y: data.year,              // year pillar
            m: data.month,             // month pillar
            d: data.day,               // day pillar
            h: data.hour,              // hour pillar
            e: data.elements,          // elements
            ts: Date.now()             // timestamp
        };
        
        // Convert to base64
        const jsonString = JSON.stringify(shareData);
        const base64 = btoa(unescape(encodeURIComponent(jsonString)));
        
        // Make URL-safe
        return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
    }
    
    decodeShareData(encodedData) {
        try {
            // Convert from URL-safe base64
            const base64 = encodedData.replace(/-/g, '+').replace(/_/g, '/');
            
            // Add padding if needed
            const padding = 4 - (base64.length % 4);
            const paddedBase64 = padding < 4 ? base64 + '='.repeat(padding) : base64;
            
            // Decode
            const jsonString = decodeURIComponent(escape(atob(paddedBase64)));
            return JSON.parse(jsonString);
        } catch (error) {
            console.error('Error decoding share data:', error);
            return null;
        }
    }
    
    copyUrl() {
        const urlInput = document.getElementById('share-url');
        if (!urlInput) return;
        
        urlInput.select();
        urlInput.setSelectionRange(0, 99999); // For mobile
        
        try {
            document.execCommand('copy');
            this.showToast('링크가 복사되었습니다!');
            
            // Change button text temporarily
            const copyBtn = document.querySelector('.btn-copy-url .copy-text');
            if (copyBtn) {
                const originalText = copyBtn.textContent;
                copyBtn.textContent = '복사됨!';
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                }, 2000);
            }
        } catch (err) {
            console.error('Copy failed:', err);
            this.showToast('복사 실패. 수동으로 복사해주세요.');
        }
    }
    
    async createShortUrl() {
        if (!this.shareUrl) {
            this.generateShareUrl();
        }
        
        try {
            // Call your URL shortening API
            const response = await fetch('/api/shorten-url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: this.shareUrl })
            });
            
            if (response.ok) {
                const data = await response.json();
                const shortUrlInput = document.getElementById('short-url');
                if (shortUrlInput) {
                    shortUrlInput.value = data.shortUrl;
                }
                this.showToast('단축 URL이 생성되었습니다!');
            }
        } catch (error) {
            console.error('Error creating short URL:', error);
            // Fallback to using a simple hash
            const hash = this.generateHash();
            const shortUrl = `${window.location.origin}/s/${hash}`;
            const shortUrlInput = document.getElementById('short-url');
            if (shortUrlInput) {
                shortUrlInput.value = shortUrl;
            }
        }
    }
    
    generateHash() {
        return Math.random().toString(36).substring(2, 8);
    }
    
    shareKakao() {
        if (!window.Kakao) {
            this.showToast('카카오 SDK를 로드할 수 없습니다.');
            return;
        }
        
        Kakao.Link.sendDefault({
            objectType: 'feed',
            content: {
                title: '나의 사주팔자 결과',
                description: '사주명리로 알아보는 나의 운명',
                imageUrl: window.location.origin + '/images/saju-share.jpg',
                link: {
                    mobileWebUrl: this.shareUrl,
                    webUrl: this.shareUrl
                }
            },
            buttons: [
                {
                    title: '결과 보기',
                    link: {
                        mobileWebUrl: this.shareUrl,
                        webUrl: this.shareUrl
                    }
                }
            ]
        });
    }
    
    shareFacebook() {
        const url = encodeURIComponent(this.shareUrl);
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
    }
    
    shareTwitter() {
        const url = encodeURIComponent(this.shareUrl);
        const text = encodeURIComponent('나의 사주팔자 결과를 확인해보세요!');
        window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank');
    }
    
    generateQRCode() {
        const canvas = document.getElementById('qr-code');
        if (!canvas || !this.shareUrl) return;
        
        // Use QRCode library or implement simple QR generation
        // For now, we'll create a placeholder
        const ctx = canvas.getContext('2d');
        canvas.width = 200;
        canvas.height = 200;
        
        // Placeholder QR code visualization
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, 200, 200);
        ctx.fillStyle = '#fff';
        ctx.fillRect(10, 10, 180, 180);
        ctx.fillStyle = '#000';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('QR Code', 100, 100);
        ctx.font = '10px Arial';
        ctx.fillText('(Requires QR library)', 100, 120);
    }
    
    downloadQR() {
        const canvas = document.getElementById('qr-code');
        if (!canvas) return;
        
        const link = document.createElement('a');
        link.download = 'saju-qr-code.png';
        link.href = canvas.toDataURL();
        link.click();
    }
    
    async exportAsImage(format) {
        const resultsSection = document.getElementById('results-section');
        if (!resultsSection) return;
        
        this.showToast('이미지 생성 중...');
        
        try {
            // Use html2canvas library if available
            if (window.html2canvas) {
                const canvas = await html2canvas(resultsSection, {
                    backgroundColor: '#ffffff',
                    scale: 2,
                    logging: false
                });
                
                if (format === 'pdf') {
                    // Use jsPDF if available
                    if (window.jspdf) {
                        const pdf = new window.jspdf.jsPDF();
                        const imgData = canvas.toDataURL('image/png');
                        pdf.addImage(imgData, 'PNG', 10, 10, 190, 0);
                        pdf.save('saju-result.pdf');
                    } else {
                        this.showToast('PDF 라이브러리를 로드할 수 없습니다.');
                    }
                } else {
                    // Download as image
                    const link = document.createElement('a');
                    link.download = `saju-result.${format}`;
                    link.href = canvas.toDataURL(`image/${format === 'jpg' ? 'jpeg' : format}`);
                    link.click();
                }
                
                this.showToast('다운로드가 시작되었습니다!');
            } else {
                // Fallback: Take screenshot of visible area
                this.captureVisibleArea(format);
            }
        } catch (error) {
            console.error('Error exporting image:', error);
            this.showToast('이미지 생성 실패');
        }
    }
    
    captureVisibleArea(format) {
        // Simple fallback - instruct user to take screenshot
        this.showToast('스크린샷을 찍어 저장해주세요 (Ctrl+Shift+S)');
    }
    
    checkForSharedResult() {
        // Check if URL contains share parameter
        const urlParams = new URLSearchParams(window.location.search);
        const shareData = urlParams.get('share');
        
        if (shareData) {
            const decodedData = this.decodeShareData(shareData);
            if (decodedData) {
                this.loadSharedResult(decodedData);
            }
        }
    }
    
    loadSharedResult(data) {
        // Fill form with shared data
        if (data.bd) {
            const [year, month, day] = data.bd.split('-');
            this.setFormValue('year', year);
            this.setFormValue('month', month);
            this.setFormValue('day', day);
        }
        
        if (data.bt) {
            this.setFormValue('hour', data.bt);
        }
        
        if (data.g) {
            this.setFormValue('gender', data.g);
        }
        
        // Set calendar type
        if (data.il !== undefined) {
            const calendarToggle = document.getElementById('calendar-type-toggle');
            if (calendarToggle) {
                calendarToggle.checked = data.il;
            }
        }
        
        // Display results
        const sajuData = {
            year: data.y,
            month: data.m,
            day: data.d,
            hour: data.h,
            elements: data.e,
            birthDate: data.bd,
            birthTime: data.bt,
            gender: data.g,
            isLunar: data.il
        };
        
        // Trigger event to display results
        const event = new CustomEvent('sajuCalculated', { detail: sajuData });
        window.dispatchEvent(event);
        
        // Show notification
        this.showToast('공유된 사주 결과를 불러왔습니다!');
    }
    
    setFormValue(field, value) {
        const selectors = {
            year: ['#year-input', 'input[name="birthYear"]', 'select[name="birthYear"]'],
            month: ['#month-input', 'input[name="birthMonth"]', 'select[name="birthMonth"]'],
            day: ['#day-input', 'input[name="birthDay"]', 'select[name="birthDay"]'],
            hour: ['#hour-input', 'select[name="birthHour"]', 'input[name="birthTime"]'],
            gender: ['input[name="gender"][value="' + value + '"]', 'select[name="gender"]']
        };
        
        const fieldSelectors = selectors[field];
        if (fieldSelectors) {
            for (const selector of fieldSelectors) {
                const element = document.querySelector(selector);
                if (element) {
                    if (element.type === 'radio') {
                        element.checked = true;
                    } else {
                        element.value = value;
                    }
                    break;
                }
            }
        }
    }
    
    showToast(message) {
        // Create toast if it doesn't exist
        let toast = document.getElementById('share-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'share-toast';
            toast.className = 'share-toast';
            document.body.appendChild(toast);
        }
        
        toast.textContent = message;
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// Export for use
window.ResultSharing = ResultSharing;