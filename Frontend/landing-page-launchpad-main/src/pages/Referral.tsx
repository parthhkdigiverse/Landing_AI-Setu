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
    const handler = (event: any) => {
      if (event.data && event.data.source === 'django-admin') {
        setContent((prev: any) => ({
          ...prev,
          ...event.data.payload
        }));
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
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

              {livePreview?.referral_title ||
                content?.referral_main_title ||
                "Referral Program"}

            </h1>

            <p className="text-primary-foreground/70 max-w-lg mx-auto">

              {livePreview?.referral_description ||
                content?.referral_main_desc ||
                "Earn money by referring retailers to AI-Setu ERP."}

            </p>

          </div>

        </div>

        <ReferralSection />
        <SolutionSection />
        <USPSection />
        <ComparisonSection />
      </main>

      <Footer />

    </>
  );

};

export default Referral;