import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const jobData: any = {
  "frontend-developer": {
    title: "Frontend Developer",
    location: "Ahmedabad",
    experience: "1-3 Years",
    description: [
      "Develop modern UI using React.",
      "Integrate APIs from backend.",
      "Work with UI/UX designers.",
      "Improve performance and responsiveness."
    ],
    skills: ["React", "JavaScript", "Tailwind", "HTML", "CSS"]
  },

  "backend-developer": {
    title: "Backend Developer (Python/Django)",
    location: "Ahmedabad",
    experience: "2-4 Years",
    description: [
      "Develop scalable REST APIs using Django.",
      "Work with databases and data models.",
      "Collaborate with frontend developers.",
      "Optimize backend performance."
    ],
    skills: ["Python", "Django", "REST API", "PostgreSQL", "Docker"]
  },

  "ai-engineer": {
    title: "AI Engineer",
    location: "Remote / Ahmedabad",
    experience: "2+ Years",
    description: [
      "Develop AI powered ERP features.",
      "Integrate machine learning models.",
      "Work with LLMs and automation.",
      "Improve business intelligence systems."
    ],
    skills: ["Python", "Machine Learning", "LLM", "TensorFlow", "PyTorch"]
  }
};

const JobDetails = () => {

  const { jobId } = useParams();
  const navigate = useNavigate(); // ✅ FIXED

  const job = jobData[jobId as keyof typeof jobData];

  if (!job) {
    return (
      <div className="text-center py-20 text-xl font-semibold">
        Job Not Found
      </div>
    );
  }

  return (
    <>
      <Header />

      <main className="bg-[#F5F6FA] min-h-screen">

        {/* HERO */}

        <section className="bg-[#1F2E4D] text-white py-16">

          <div className="container mx-auto px-6 max-w-4xl">

            <motion.h1
              initial={{ opacity: 0, y: -40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-4xl font-bold mb-4"
            >
              {job.title}
            </motion.h1>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="opacity-80 text-lg"
            >
              {job.experience} • {job.location}
            </motion.p>

          </div>

        </section>


        {/* JOB DETAILS CARD */}

        <section className="py-20">

          <div className="container mx-auto px-6 max-w-4xl">

            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="bg-white p-10 rounded-xl shadow-lg space-y-10"
            >

              {/* Description */}

              <div>

                <h2 className="text-2xl font-semibold mb-6 text-[#1F2E4D]">
                  Job Description
                </h2>

                <ul className="space-y-3">

                  {job.description.map((item: string, i: number) => (

                    <motion.li
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="flex items-start gap-3 text-gray-700"
                    >

                      <span className="text-[#F4B400] font-bold text-lg">
                        •
                      </span>

                      {item}

                    </motion.li>

                  ))}

                </ul>

              </div>


              {/* Skills */}

              <div>

                <h2 className="text-2xl font-semibold mb-6 text-[#1F2E4D]">
                  Required Skills
                </h2>

                <div className="flex flex-wrap gap-3">

                  {job.skills.map((skill: string, i: number) => (

                    <motion.span
                      key={i}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: i * 0.1 }}
                      whileHover={{ scale: 1.1 }}
                      className="bg-[#FFF3CD] text-[#1F2E4D] px-4 py-2 rounded-lg font-medium shadow-sm cursor-default"
                    >
                      {skill}
                    </motion.span>

                  ))}

                </div>

              </div>


              {/* Apply Button */}

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate(`/career/apply/${jobId}`)}
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