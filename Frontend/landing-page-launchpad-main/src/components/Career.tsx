import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Briefcase, Users, Rocket, HeartHandshake } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useRef } from "react";

const jobs = [
  {
    title: "Frontend Developer",
    exp: "1-3 Years",
    location: "Ahmedabad",
    slug: "frontend-developer",
  },
  {
    title: "Backend Developer (Python/Django)",
    exp: "2-4 Years",
    location: "Ahmedabad",
    slug: "backend-developer",
  },
  {
    title: "AI Engineer",
    exp: "2+ Years",
    location: "Remote / Ahmedabad",
    slug: "ai-engineer",
  },
];

const CareerPage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const openingsRef = useRef<HTMLDivElement>(null);

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
            Build Your Career With AI-Setu 🚀
          </motion.h1>

          <p className="max-w-2xl mx-auto text-lg opacity-90">
            Join a team building the future of AI powered ERP systems.
            Work with innovative people and solve real business problems.
          </p>

        </section>

        {/* CULTURE */}

        <section className="py-20 container mx-auto px-6">

          <h2 className="text-4xl font-bold text-center mb-14 text-[#1F2E4D]">
            Our Culture
          </h2>

          <div className="grid md:grid-cols-4 gap-8">

            {[
              {
                icon: Users,
                title: "Collaboration",
                desc: "We believe teamwork builds better solutions.",
              },
              {
                icon: Rocket,
                title: "Innovation",
                desc: "Experiment and create new possibilities.",
              },
              {
                icon: Briefcase,
                title: "Growth",
                desc: "Continuous learning and career growth.",
              },
              {
                icon: HeartHandshake,
                title: "Trust",
                desc: "Transparency and respect always.",
              },
            ].map((item, i) => (
              <motion.div
                key={i}
                whileHover={{ scale: 1.06 }}
                className="bg-white p-8 rounded-xl shadow-md text-center"
              >
                <item.icon
                  className="mx-auto mb-4 text-[#F4B400]"
                  size={40}
                />

                <h3 className="font-semibold text-xl mb-2 text-[#1F2E4D]">
                  {item.title}
                </h3>

                <p className="text-gray-600">
                  {item.desc}
                </p>

              </motion.div>
            ))}

          </div>

        </section>

        {/* BENEFITS */}

        <section className="py-20 bg-white">

          <div className="container mx-auto px-6 text-center">

            <h2 className="text-4xl font-bold mb-12 text-[#1F2E4D]">
              Perks & Benefits
            </h2>

            <div className="grid md:grid-cols-3 gap-8">

              {[
                "Flexible Work Culture",
                "5 Day Work Week",
                "Learning Budget",
                "Team Events",
                "Fast Career Growth",
                "Friendly Work Environment",
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
            Open Positions
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

                  <p className="text-gray-500">
                    {job.exp} • {job.location}
                  </p>

                </div>

                <span className="text-[#F4B400] font-semibold">
                  View →
                </span>

              </motion.div>

            ))}

          </div>

        </section>

        {/* CTA */}

        <section className="py-20 text-center bg-[#1F2E4D] text-white">

          <h2 className="text-4xl font-bold mb-4">
            Ready to Join AI-Setu?
          </h2>

          <p className="mb-8">
            Explore our current openings and apply today.
          </p>

          <button
            onClick={() =>
              openingsRef.current?.scrollIntoView({ behavior: "smooth" })
            }
            className="bg-gradient-to-r from-[#F4B400] to-[#F6C34A] text-black font-bold px-8 py-4 rounded-lg shadow hover:scale-105 transition"
          >
            View Openings
          </button>

        </section>

      </main>

      <Footer />
    </>
  );
};

export default CareerPage;