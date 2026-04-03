import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SEO from "@/components/SEO";
import { motion } from "framer-motion";
import DynamicIcon from "@/components/DynamicIcon";
import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { fetchCareerPageContent, CareerPageContent } from "@/services/api";

import { JobSkeleton } from "@/components/landing/LandingSkeleton";

const CareerPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const openingsRef = useRef<HTMLDivElement>(null);
  const [isPreview, setIsPreview] = useState(false);
  const [targetSection, setTargetSection] = useState<string | null>(null);
  const [content, setContent] = useState<CareerPageContent | null>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  // ... (previous effects)

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const isP = params.get('is_preview') === "1";
    setIsPreview(isP);
    if (isP) {
      setTargetSection(params.get('section') || 'all');
    }
  }, []);

  const shouldShowSection = (sectionName: string) => {
    if (!targetSection || targetSection === 'all') return true;
    return targetSection === sectionName;
  };

  useEffect(() => {
    if (targetSection && targetSection !== 'all') {
      setTimeout(() => {
        const el = document.getElementById(targetSection);
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 800);
    }
  }, [targetSection]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchCareerPageContent();
        if (data) setContent(data);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, []);

  useEffect(() => {
    const previewChannel = new BroadcastChannel('aisetu_preview');

    const handleMessage = (event: MessageEvent) => {
      if (event.data === "reload_full_data") {
        fetchCareerPageContent().then((data) => data && setContent(data));
      } else if (event.data && typeof event.data === 'object' && event.data.source === 'django-admin') {
        
        const payload = event.data.payload;
        const model = event.data.model;
        let parsedPayload = { ...payload };

        if (model === 'CareerPage' || model === 'CareerPageContent' || 
            ['careerherocontent', 'careerculturecontent', 'careerperkscontent', 'careerjobscontent', 'careerctacontent'].includes(model.toLowerCase())) {
          // Deserialize dynamic Inline Formsets into structural React Arrays
          const cultures: any[] = [];
          const perks: any[] = [];
          const jobs: any[] = [];

          Object.keys(payload).forEach(key => {
              if (key.includes('TOTAL_FORMS') || key.includes('INITIAL_FORMS') || key.includes('MAX_NUM_FORMS') || key.includes('MIN_NUM_FORMS')) return;

              if (key.startsWith('cultures-')) {
                  const parts = key.split('-');
                  if (parts.length >= 3) {
                      const idx = parseInt(parts[1], 10);
                      const field = parts.slice(2).join('-');
                      if (!cultures[idx]) cultures[idx] = {};
                      cultures[idx][field] = payload[key];
                  }
              } else if (key.startsWith('perks-')) {
                  const parts = key.split('-');
                  if (parts.length >= 3) {
                      const idx = parseInt(parts[1], 10);
                      const field = parts.slice(2).join('-');
                      if (!perks[idx]) perks[idx] = {};
                      perks[idx][field] = payload[key];
                  }
              } else if (key.startsWith('jobs-')) {
                  const parts = key.split('-');
                  if (parts.length >= 3) {
                      const idx = parseInt(parts[1], 10);
                      const field = parts.slice(2).join('-');
                      if (!jobs[idx]) jobs[idx] = {};
                      jobs[idx][field] = payload[key];
                      if (field === 'slug') jobs[idx].job_slug = payload[key];
                  }
              }
          });

          parsedPayload = { 
              ...payload, 
              cultures: cultures.filter((item: any) => item && !item.DELETE),
              perks: perks.filter((item: any) => item && !item.DELETE),
              jobs: jobs.filter((item: any) => item && !item.DELETE)
          };

          setLivePreview((prev: any) => ({ ...prev, ...parsedPayload }));
          
          // Broadcast to other tabs
          previewChannel.postMessage({
              type: 'LIVE_PREVIEW_UPDATE',
              model: 'CareerPage',
              content: parsedPayload
          });

        } else if (model === 'ChildJobPosition') {
          // Handle specific job position update in the list (Upsert/Delete)
          setLivePreview((prev: any) => {
            const currentJobs = prev?.jobs || content?.jobs || [];
            let found = false;
            let updatedJobs = currentJobs.map((j: any) => {
               // Match by slug, job_slug, or title (if slug is missing in payload)
               const isMatch = (payload.slug && (j.slug === payload.slug || j.job_slug === payload.slug)) || 
                               (!payload.slug && j.title === payload.title);
               
               if (isMatch) {
                   found = true;
                   return { ...j, ...payload };
               }
               return j;
            });

            if (!found && !payload.DELETE) {
                // If not found, it's a NEW job being created/previewed.
                updatedJobs = [...updatedJobs, { ...payload, is_new: true }];
            }

            // FILTER: Remove jobs that are marked for deletion
            updatedJobs = updatedJobs.filter((j: any) => !j.DELETE);
            
            const newPreview = { ...prev, jobs: updatedJobs };
            
            // Broadcast the update for other components
            previewChannel.postMessage({
              type: 'LIVE_PREVIEW_UPDATE',
              model: 'ChildJobPosition',
              content: payload
            });
            
            return newPreview;
          });
        }

        if (event.data.scrollTarget) {
            setTimeout(() => {
                const el = document.getElementById(event.data.scrollTarget);
                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        }
      }
    };

    const handleChannelMessage = (event: MessageEvent) => {
      if (event.data?.type === 'LIVE_PREVIEW_UPDATE') {
        if (event.data.model === 'CareerPage') {
          setLivePreview((prev: any) => ({ ...prev, ...event.data.content }));
        } else if (event.data.model === 'ChildJobPosition') {
          const payload = event.data.content;
          setLivePreview((prev: any) => {
            const currentJobs = prev?.jobs || content?.jobs || [];
            const updatedJobs = currentJobs.map((j: any) => 
               (j.slug === payload.slug || j.job_slug === payload.slug) ? { ...j, ...payload } : j
            );
            return { ...prev, jobs: updatedJobs };
          });
        }
      }
    };

    window.addEventListener("message", handleMessage);
    previewChannel.addEventListener("message", handleChannelMessage);

    return () => {
      window.removeEventListener("message", handleMessage);
      previewChannel.removeEventListener("message", handleChannelMessage);
      previewChannel.close();
    };
  }, [content]);

  useEffect(() => {
    if (location.hash === "#openings") {
      openingsRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [location]);

  if (isLoading && !content && !isPreview) {
    return (
      <>
        <Header />
        <main className="bg-[#F5F6FA] min-h-screen">
          <JobSkeleton />
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <SEO 
        title={content?.seo_title || "Careers"} 
        description={content?.seo_description || "Join AI Setu and help us build the future of AI-driven retail solutions. Explore our open positions and grow with us."}
        keywords={content?.seo_keywords || "careers, jobs, AI Setu hiring, retail tech roles"}
      />
      {(!isPreview || targetSection === 'all' || !targetSection) && <Header />}

      <main className="bg-[#F5F6FA]">

        {/* HERO */}
        {shouldShowSection('hero') && (
        <section id="hero" className="py-24 text-center bg-[#1F2E4D] text-white">
          <motion.h1
            initial={{ opacity: 0, y: -40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-5xl font-bold mb-6"
          >
            {livePreview?.hero_title || content?.hero_title || "Build Your Career With AI-Setu 🚀"}
          </motion.h1>

          <p className="max-w-2xl mx-auto text-lg opacity-90">
            {livePreview?.hero_subtitle || content?.hero_subtitle ||
              "Join a team building the future of AI powered ERP systems."}
          </p>
        </section>
        )}

        {/* CULTURE */}
        {shouldShowSection('culture') && (
        <section id="culture" className="py-20 container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-14 text-[#1F2E4D]">
            {livePreview?.culture_title || content?.culture_title || "Our Culture"}
          </h2>

          <div className="grid md:grid-cols-4 gap-8">
            {(livePreview?.cultures || content?.cultures)?.map((item: any, i: number) => (
              <motion.div
                key={i}
                whileHover={{ scale: 1.06 }}
                className="bg-white p-8 rounded-xl shadow-md text-center"
              >
                <DynamicIcon 
                  name={item.icon || (i === 0 ? "Users" : i === 1 ? "Rocket" : i === 2 ? "Briefcase" : "HeartHandshake")} 
                  size={40} 
                  className="mx-auto mb-4 text-[#F4B400]" 
                />
                <h3 className="font-semibold text-xl mb-2 text-[#1F2E4D]">
                  {item.title}
                </h3>
                <p className="text-gray-600">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </section>
        )}

        {/* BENEFITS */}
        {shouldShowSection('perks') && (
        <section id="perks" className="py-20 bg-white">
          <div className="container mx-auto px-6 text-center">
            <h2 className="text-4xl font-bold mb-12 text-[#1F2E4D]">
              {livePreview?.perks_title || content?.perks_title || "Perks & Benefits"}
            </h2>

            <div className="grid md:grid-cols-3 gap-8">
              {(livePreview?.perks || content?.perks)?.map((perk: any, i: number) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4 }}
                  className="bg-[#F5F6FA] p-6 rounded-lg shadow-sm"
                >
                  {perk.title}
                </motion.div>
              ))}
            </div>
          </div>
        </section>
        )}

        {/* JOB POSITIONS */}
        {shouldShowSection('jobs') && (
        <section
          id="open_positions"
          ref={openingsRef}
          className="py-20 container mx-auto px-6"
        >
          <h2 className="text-4xl font-bold text-center mb-12 text-[#1F2E4D]">
            {livePreview?.positions_title || content?.positions_title || "Open Positions"}
          </h2>

          <div className="space-y-6">
            {(livePreview?.jobs || content?.jobs)?.map((job: any, index: number) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.02 }}
                onClick={() => navigate(`/career/${job.job_slug}`)}
                className="bg-white shadow-md rounded-lg p-6 flex justify-between items-center cursor-pointer hover:border hover:border-[#F4B400] transition"
              >
                <div>
                  <h3 className="text-xl font-semibold text-[#1F2E4D]">
                    {job.title}
                  </h3>
                  <p className="text-gray-500">
                    {job.experience} • {job.total_positions} Positions • {job.work_place} • {job.location}
                  </p>
                </div>
                <span className="text-[#F4B400] font-semibold">View →</span>
              </motion.div>
            ))}
          </div>
        </section>
        )}

        {/* CTA */}
        {shouldShowSection('cta') && (
        <section id="cta" className="py-20 text-center bg-[#1F2E4D] text-white">
          <h2 className="text-4xl font-bold mb-4">
            {livePreview?.cta_title || content?.cta_title || "Ready to Join AI-Setu?"}
          </h2>

          <p className="mb-8">
            {livePreview?.cta_subtitle || content?.cta_subtitle ||
              "Explore our current openings and apply today."}
          </p>

          <button
            onClick={() =>
              openingsRef.current?.scrollIntoView({ behavior: "smooth" })
            }
            className="bg-gradient-to-r from-[#F4B400] to-[#F6C34A] text-black font-bold px-8 py-4 rounded-lg shadow hover:scale-105 transition"
          >
            {livePreview?.cta_button_text || content?.cta_button_text || "View Openings"}
          </button>
        </section>
        )}
      </main>

      {!isPreview && <Footer />}
    </>
  );
};

export default CareerPage;