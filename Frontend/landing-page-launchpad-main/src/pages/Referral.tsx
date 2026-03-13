import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ReferralSection from "@/components/landing/ReferralSection";
import FAQSection from "@/components/landing/FAQSection";

import { useState, useEffect } from "react";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

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

    const handler = (event:any) => {

      if(event.data){
        setContent((prev:any)=>({
          ...prev,
          ...event.data
        }))
      }

    }

    window.addEventListener("message", handler)

    return () => window.removeEventListener("message", handler)

  },[])


  return (

    <>
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
        <FAQSection />

      </main>

      <Footer />

    </>
  );

};

export default Referral;