import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SolutionSection from "@/components/landing/SolutionSection";
import USPSection from "@/components/landing/USPSection";
import ComparisonSection from "@/components/landing/ComparisonSection";

import { useState, useEffect } from "react";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";
import SEO from "@/components/SEO";

const Features = () => {

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
      }
    };

    window.addEventListener("message", handler)

    return () => window.removeEventListener("message", handler)

  },[])


  return (

    <>
      <SEO 
        title={content?.seo_title || "Features"} 
        description={content?.seo_description || "Discover how AI Setu transforms retail with AI scanning, automated billing, and smart inventory management. Explore our cutting-edge features."}
        keywords={content?.seo_keywords || "AI scanning, automated billing, inventory management, retail tech"}
      />
      <Header />

      <main>

        {/* HERO */}

        <div className="bg-hero text-primary-foreground py-16 text-center">

          <div className="container">

            <h1 className="text-4xl lg:text-5xl font-extrabold mb-4">

              {livePreview?.feature_title ||
                content?.feature_title ||
                "Features"}

            </h1>

            <p className="text-primary-foreground/70 max-w-lg mx-auto">

              {livePreview?.feature_title2 ||
                content?.feature_title2 ||
                "Everything you need to run your retail business smarter."}

            </p>

          </div>

        </div>

        <SolutionSection />
        <USPSection />
        <ComparisonSection />

      </main>

      <Footer />

    </>
  );

};

export default Features;