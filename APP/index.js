 document.querySelectorAll('nav a').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        window.scrollTo({
          top: targetSection.offsetTop,
          behavior: 'smooth'
        });
      });
    });
    
   
    document.querySelectorAll('.feature-card').forEach((card, index) => {
      card.style.transitionDelay = `${index * 0.1}s`;
    });
    
    
    function resizeVideo() {
      const video = document.querySelector('.video-bg');
      const aspectRatio = 16/9;
      
      if (window.innerWidth / window.innerHeight > aspectRatio) {
        video.style.width = '100%';
        video.style.height = 'auto';
      } else {
        video.style.width = 'auto';
        video.style.height = '100%';
      }
    }
    
    window.addEventListener('load', resizeVideo);
    window.addEventListener('resize', resizeVideo);