import React from 'react';
import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title?: string;
  description?: string;
  keywords?: string;
  ogImage?: string;
  ogUrl?: string;
  ogType?: string;
}

const SEO: React.FC<SEOProps> = ({
  title,
  description,
  keywords,
  ogImage,
  ogUrl,
  ogType = 'website',
}) => {
  const siteTitle = 'AI-Setu ERP';
  const fullTitle = title ? `${title} | ${siteTitle}` : 'AI-Setu ERP – Smart ERP for Indian Retailers';
  const defaultDescription = 'AI-powered billing, inventory & store management ERP built for Indian retail businesses. GST ready, cloud-based, 24/7 support.';
  const currentUrl = ogUrl || window.location.href;
  const defaultOgImage = 'https://lovable.dev/opengraph-image-p98pqg.png';

  return (
    <Helmet>
      {/* Standard metadata tags */}
      <title>{fullTitle}</title>
      <meta name="description" content={description || defaultDescription} />
      {keywords && <meta name="keywords" content={keywords} />}
      <link rel="canonical" href={currentUrl} />

      {/* Open Graph / Facebook */}
      <meta property="og:type" content={ogType} />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description || defaultDescription} />
      <meta property="og:image" content={ogImage || defaultOgImage} />
      <meta property="og:url" content={currentUrl} />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description || defaultDescription} />
      <meta name="twitter:image" content={ogImage || defaultOgImage} />
    </Helmet>
  );
};

export default SEO;
