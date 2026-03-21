import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import SEO from "@/components/SEO";

interface Job {
  title: string;
  slug: string;
  location: string;
  experience: string;
  descriptions: { text: string }[];
  skills: { name: string }[];
  seo_title?: string;
  seo_description?: string;
  seo_keywords?: string;
}

const JobDetails = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();

  const [job, setJob] = useState<Job | null>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const isPreviewMode = jobId === "new-job";

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data && typeof event.data === 'object' && event.data.source === 'django-admin') {
        setLivePreview((prev: any) => ({ ...prev, ...event.data.payload }));
        if (event.data.scrollTarget) {
            setTimeout(() => {
                const el = document.getElementById(event.data.scrollTarget);
                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        }
      }
    };

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, []);

  useEffect(() => {
    if (!jobId) {
      setError("Invalid job link");
      setLoading(false);
      return;
    }

    if (isPreviewMode) {
      // Create a dummy job to populate the UI
      setJob({
        title: "New Job Position",
        slug: "new-job",
        location: "Location",
        experience: "Experience Level",
        descriptions: [],
        skills: [],
      });
      setLoading(false);
      return;
    }

    const fetchJob = async () => {
      try {
        const response = await fetch(
          `/api/job/${jobId}/`
        );

        if (!response.ok) {
          throw new Error("Job not found");
        }

        const data = await response.json();
        setJob(data);
      } catch (err) {
        console.error("Error loading job:", err);
        setError("Failed to load job details");
      } finally {
        setLoading(false);
      }
    };

    fetchJob();
  }, [jobId, isPreviewMode]);

  if (loading) {
    return (
      <>
        <Header />
        <div className="text-center py-24 text-xl font-semibold">
          Loading Job...
        </div>
        <Footer />
      </>
    );
  }

  if (error || !job) {
    return (
      <>
        <Header />
        <div className="text-center py-24 text-xl font-semibold text-red-500">
          {error || "Job Not Found"}
        </div>
        <Footer />
      </>
    );
  }

  return (
    <>
      <SEO 
        title={job.seo_title || `${job.title} | Careers`} 
        description={job.seo_description || `We are hiring for the position of ${job.title} in ${job.location}. Experience required: ${job.experience}. Apply now to join AI Setu!`}
        keywords={job.seo_keywords || `${job.title}, ${job.location}, career, job opening`}
      />
      <Header />

      <main className="bg-[#F5F6FA] min-h-screen">

        {/* HERO */}
        <section id="job_header" className="bg-[#1F2E4D] text-white py-16">
          <div className="container mx-auto px-6 max-w-4xl">

            <motion.h1
              initial={{ opacity: 0, y: -40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-4xl font-bold mb-4"
            >
              {livePreview?.title || job.title}
            </motion.h1>

            <p className="opacity-80 text-lg">
              {livePreview?.experience || job.experience} • {livePreview?.location || job.location}
            </p>

          </div>
        </section>

        {/* DETAILS */}
        <section className="py-20">
          <div className="container mx-auto px-6 max-w-4xl">

            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white p-10 rounded-xl shadow-lg space-y-10"
            >

              {/* DESCRIPTION */}
              <div id="job_description">
                <h2 className="text-2xl font-semibold mb-6 text-[#1F2E4D]">
                  Job Description
                </h2>

                <ul className="space-y-3">
                  {job.descriptions?.map((item, i) => (
                    <motion.li
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="flex items-start gap-3 text-gray-700"
                    >
                      <span className="text-[#F4B400] font-bold">•</span>
                      {item.text}
                    </motion.li>
                  ))}
                </ul>
              </div>

              {/* SKILLS */}
              <div id="job_skills">
                <h2 className="text-2xl font-semibold mb-6 text-[#1F2E4D]">
                  Required Skills
                </h2>

                <div className="flex flex-wrap gap-3">
                  {job.skills?.map((skill, i) => (
                    <motion.span
                      key={i}
                      whileHover={{ scale: 1.1 }}
                      className="bg-[#FFF3CD] text-[#1F2E4D] px-4 py-2 rounded-lg font-medium shadow-sm"
                    >
                      {skill.name}
                    </motion.span>
                  ))}
                </div>
              </div>

              {/* APPLY BUTTON */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate(`/career/apply/${job.slug}`)}
                className="bg-gradient-to-r from-[#F4B400] to-[#F6C34A] text-black font-bold px-8 py-4 rounded-lg shadow-md hover:shadow-xl transition"
              >
                Apply For This Job
              </motion.button>

            </motion.div>
          </div>
        </section>

      </main>

      <Footer />
    </>
  );
};

export default JobDetails;