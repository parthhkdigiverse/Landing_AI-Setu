import Header from "@/components/Header";
import Footer from "@/components/Footer";
import PricingSection from "@/components/landing/PricingSection";
import FAQSection from "@/components/landing/FAQSection";

import { useState, useEffect } from "react";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";
import SEO from "@/components/SEO";

const Pricing = () => {

  const [content, setContent] = useState<LandingPageContent | null>(null);
  const [livePreview, setLivePreview] = useState<any>(null);

  useEffect(() => {

    const loadContent = async () => {

      const data = await fetchLandingPageContent();

      if (data) {
        setContent(data);
      }

    };

    loadContent();

  }, []);


  // LIVE ADMIN PREVIEW
  useEffect(() => {

    const handler = (event: MessageEvent) => {
      if (event.data && typeof event.data === 'object' && !Array.isArray(event.data) && event.data.source === 'django-admin') {
        setContent((prev: any) => ({
          ...prev,
          ...event.data.payload
        }));
        if (event.data.scrollTarget) {
          setTimeout(() => {
            const el = document.getElementById(event.data.scrollTarget);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }, 100);
        }
      }
    };

    window.addEventListener("message", handler);

    return () => window.removeEventListener("message", handler);

  }, []);


  const isPreview = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('is_preview') === '1' : false;

  return (

    <>
      <SEO 
        title={content?.seo_title || "Pricing"} 
        description={content?.seo_description || "Simple and transparent pricing for businesses of all sizes. Choose the plan that fits your needs and start scaling with AI Setu today."}
        keywords={content?.seo_keywords || "AI Setu pricing, subscription plans, business automation cost"}
      />
      <Header />

      <main>

        {/* HERO */}

        <div className="bg-hero text-primary-foreground py-16 text-center">

          <div className="container">

            <h1 className="text-4xl lg:text-5xl font-extrabold mb-4">

              {livePreview?.pricing_title ||
                content?.pricing_main_title ||
                "Pricing"}

            </h1>

            <p className="text-primary-foreground/70 max-w-lg mx-auto">

              {livePreview?.pricing_description ||
                content?.pricing_main_desc ||
                "Simple, transparent pricing — one package, everything included."}

            </p>

          </div>

        </div>

        <PricingSection />
        <FAQSection />

      </main>

      <Footer />
    </>
  );
};

export default Pricing;