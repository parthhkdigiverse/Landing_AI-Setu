import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Briefcase, Users, Rocket, HeartHandshake } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useRef, useState } from "react"; // Added useState
import { fetchCareerPageContent, CareerPageContent } from "@/services/api";

const CareerPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const openingsRef = useRef<HTMLDivElement>(null);

  // --- LIVE PREVIEW & DATA STATE ---
  const [content, setContent] = useState<CareerPageContent | null>(null);

  // 1. Fetch saved content from Django on load
  useEffect(() => {
    const loadData = async () => {
      const data = await fetchCareerPageContent();
      if (data) setContent(data);
    };
    loadData();
  }, []);

  // 2. Listen for Live Preview updates from Django Admin
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data && typeof event.data === "object") {
        setContent((prev) => ({
          ...prev,
          ...event.data,
        } as CareerPageContent));
      }
      // Re-fetch everything if admin signals a Save happened
      if (event.data === "reload_full_data") {
        fetchCareerPageContent().then((data) => data && setContent(data));
      }
    };

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, []);

  // Dynamically build the jobs list from state
  const jobs = [
    {
      title: content?.job_1_role || "Frontend Developer",
      exp: content?.job_1_details || "1-3 Years • Ahmedabad",
      slug: "frontend-developer",
    },
    {
      title: content?.job_2_role || "Backend Developer (Python/Django)",
      exp: content?.job_2_details || "2-4 Years • Ahmedabad",
      slug: "backend-developer",
    },
    {
      title: content?.job_3_role || "AI Engineer",
      exp: content?.job_3_details || "2+ Years • Remote / Ahmedabad",
      slug: "ai-engineer",
    },
  ];

  // Scroll to openings when URL contains #openings
  useEffect(() => {
    if (location.hash === "#openings") {
      openingsRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [location]);

  return (
    <>
      <Header />

      <main className="bg-[#F5F6FA]">
        {/* HERO SECTION */}
        <section className="py-24 text-center bg-[#1F2E4D] text-white">
          <motion.h1
            initial={{ opacity: 0, y: -40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-5xl font-bold mb-6"
          >
            {content?.hero_title || "Build Your Career With AI-Setu 🚀"}
          </motion.h1>

          <p className="max-w-2xl mx-auto text-lg opacity-90">
            {content?.hero_description || "Join a team building the future of AI powered ERP systems. Work with innovative people and solve real business problems."}
          </p>
        </section>

        {/* CULTURE */}
        <section className="py-20 container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-14 text-[#1F2E4D]">
            {content?.culture_title || "Our Culture"}
          </h2>

          <div className="grid md:grid-cols-4 gap-8">
            {[
              {
                icon: Users,
                title: content?.culture_1_title || "Collaboration",
                desc: content?.culture_1_desc || "We believe teamwork builds better solutions.",
              },
              {
                icon: Rocket,
                title: content?.culture_2_title || "Innovation",
                desc: content?.culture_2_desc || "Experiment and create new possibilities.",
              },
              {
                icon: Briefcase,
                title: content?.culture_3_title || "Growth",
                desc: content?.culture_3_desc || "Continuous learning and career growth.",
              },
              {
                icon: HeartHandshake,
                title: content?.culture_4_title || "Trust",
                desc: content?.culture_4_desc || "Transparency and respect always.",
              },
            ].map((item, i) => (
              <motion.div
                key={i}
                whileHover={{ scale: 1.06 }}
                className="bg-white p-8 rounded-xl shadow-md text-center"
              >
                <item.icon className="mx-auto mb-4 text-[#F4B400]" size={40} />
                <h3 className="font-semibold text-xl mb-2 text-[#1F2E4D]">
                  {item.title}
                </h3>
                <p className="text-gray-600">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* BENEFITS */}
        <section className="py-20 bg-white">
          <div className="container mx-auto px-6 text-center">
            <h2 className="text-4xl font-bold mb-12 text-[#1F2E4D]">
              {content?.benefits_title || "Perks & Benefits"}
            </h2>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                content?.benefit_1 || "Flexible Work Culture",
                content?.benefit_2 || "5 Day Work Week",
                content?.benefit_3 || "Learning Budget",
                content?.benefit_4 || "Team Events",
                content?.benefit_5 || "Fast Career Growth",
                content?.benefit_6 || "Friendly Work Environment",
              ].map((benefit, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4 }}
                  className="bg-[#F5F6FA] p-6 rounded-lg shadow-sm"
                >
                  {benefit}
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* OPEN POSITIONS */}
        <section
          id="openings"
          ref={openingsRef}
          className="py-20 container mx-auto px-6"
        >
          <h2 className="text-4xl font-bold text-center mb-12 text-[#1F2E4D]">
            {content?.positions_title || "Open Positions"}
          </h2>

          <div className="space-y-6">
            {jobs.map((job, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.02 }}
                onClick={() => navigate(`/career/${job.slug}`)}
                className="bg-white shadow-md rounded-lg p-6 flex justify-between items-center cursor-pointer hover:border hover:border-[#F4B400] transition"
              >
                <div>
                  <h3 className="text-xl font-semibold text-[#1F2E4D]">
                    {job.title}
                  </h3>
                  <p className="text-gray-500">{job.exp}</p>
                </div>
                <span className="text-[#F4B400] font-semibold">View →</span>
              </motion.div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="py-20 text-center bg-[#1F2E4D] text-white">
          <h2 className="text-4xl font-bold mb-4">
            {content?.cta_title || "Ready to Join AI-Setu?"}
          </h2>

          <p className="mb-8">
            {content?.cta_description || "Explore our current openings and apply today."}
          </p>

          <button
            onClick={() =>
              openingsRef.current?.scrollIntoView({ behavior: "smooth" })
            }
            className="bg-gradient-to-r from-[#F4B400] to-[#F6C34A] text-black font-bold px-8 py-4 rounded-lg shadow hover:scale-105 transition"
          >
            {content?.cta_button_text || "View Openings"}
          </button>
        </section>
      </main>

      <Footer />
    </>
  );
};

export default CareerPage;