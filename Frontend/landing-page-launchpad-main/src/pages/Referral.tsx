import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ReferralSection from "@/components/landing/ReferralSection";
import SolutionSection from "@/components/landing/SolutionSection";
import USPSection from "@/components/landing/USPSection";
import ComparisonSection from "@/components/landing/ComparisonSection";

import { useState, useEffect } from "react";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";
import SEO from "@/components/SEO";

const Referral = () => {

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
    const previewChannel = new BroadcastChannel('aisetu_preview');

    const handler = (event: any) => {
      if (event.data && typeof event.data === 'object' && event.data.source === 'django-admin') {
        const payload = event.data.payload;
        
        setContent((prev: any) => ({
          ...prev,
          ...payload
        }));

        // Broadcast to other tabs
        previewChannel.postMessage({
          type: 'LIVE_PREVIEW_UPDATE',
          model: event.data.model,
          content: payload
        });
      }
    };

    const channelHandler = (event: MessageEvent) => {
      if (event.data?.type === 'LIVE_PREVIEW_UPDATE') {
        setContent((prev: any) => ({
          ...prev,
          ...event.data.content
        }));
      }
    };

    window.addEventListener("message", handler);
    previewChannel.addEventListener("message", channelHandler);

    return () => {
      window.removeEventListener("message", handler);
      previewChannel.removeEventListener("message", channelHandler);
      previewChannel.close();
    };
  }, []);

  const isPreview = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('is_preview') === '1' : false;

  return (

    <>
      <SEO 
        title="Referral Program" 
        description="Join the AI Setu Referral Program and earn rewards for every business you refer. Help local retailers grow with modern AI solutions."
        keywords="referral program, earn money, business partner, AI Setu rewards"
      />
      <Header />

      <main>

        {/* HERO */}

        <div className="bg-hero text-primary-foreground py-16 text-center">

          <div className="container">

            <h1 className="text-4xl lg:text-5xl font-extrabold mb-4">
              {content?.referral_main_title || "Referral Program"}
            </h1>

            <p className="text-primary-foreground/70 max-w-lg mx-auto">
              {content?.referral_main_desc || "Earn money by referring retailers to AI-Setu ERP."}
            </p>

          </div>

        </div>

        <ReferralSection />
        {!isPreview && (
          <>
            <SolutionSection />
            <USPSection />
            <ComparisonSection />
          </>
        )}
      </main>

      {!isPreview && <Footer />}

    </>
  );

};

export default Referral;