import React, { useEffect } from 'react';

const PreviewClickListener: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  useEffect(() => {
    const isPreview = window.location.search.includes('is_preview=1');
    if (!isPreview) return;

    const handleClick = (e: MouseEvent) => {
      // Find the closest element with an ID that isn't the body or main
      let target = e.target as HTMLElement;
      let sectionId = '';
      
      while (target && target !== document.body) {
        if (target.id && !['root', 'main', 'app'].includes(target.id.toLowerCase())) {
          sectionId = target.id;
          break;
        }
        target = target.parentElement as HTMLElement;
      }
      
      if (sectionId) {
        // Only prevent default if it looks like a section we want to edit
        // We allow buttons and links to work unless they are just containers
        console.log("Preview click detected on section:", sectionId);
        
        window.parent.postMessage({
          source: 'django-admin-click',
          target: sectionId
        }, '*');
      }
    };

    document.addEventListener('click', handleClick, true);
    
    const style = document.createElement('style');
    style.innerHTML = `
      [id]:not(#root):not(main):not(body):hover {
        outline: 2px dashed #F4B400 !important;
        outline-offset: -2px;
        cursor: pointer !important;
        position: relative;
      }
      [id]:not(#root):not(main):not(body):hover::after {
        content: "Click to Edit";
        position: absolute;
        top: 0;
        right: 0;
        background: #F4B400;
        color: white;
        font-size: 10px;
        padding: 2px 6px;
        font-weight: bold;
        z-index: 9999;
        pointer-events: none;
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.removeEventListener('click', handleClick, true);
      if (style.parentNode) {
        document.head.removeChild(style);
      }
    };
  }, []);

  return <>{children}</>;
};

export default PreviewClickListener;
