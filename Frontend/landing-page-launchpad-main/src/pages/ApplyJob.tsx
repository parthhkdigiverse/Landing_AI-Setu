import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";
import { toast } from "sonner";
import { API_BASE_URL } from "@/services/api";

const ApplyJob = () => {
  const navigate = useNavigate();
  const { jobId } = useParams();

  const [resume, setResume] = useState<File | null>(null);

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    experience: "",
    available_to_join: "",
    current_salary: "",
    expected_salary: "",
    location: ""
  });

  const handleChange = (e: any) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleFileChange = (e: any) => {
    setResume(e.target.files[0]);
  };

  const handleSubmit = async () => {

    if (!formData.first_name || !formData.last_name || !formData.email || !formData.phone || !resume ) {
      toast.error("Please fill required fields");
      return;
    }

    const data = new FormData();

    data.append("job_position", jobId || "");
    data.append("first_name", formData.first_name);
    data.append("last_name", formData.last_name);
    data.append("email", formData.email);
    data.append("phone", formData.phone);
    data.append("experience", formData.experience);
    data.append("available_to_join", formData.available_to_join);
    data.append("current_salary", formData.current_salary);
    data.append("expected_salary", formData.expected_salary);
    data.append("location", formData.location);

    if (resume) {
      data.append("resume", resume);
    }

    try {

      const response = await fetch(`${API_BASE_URL}/apply-job/`, {
        method: "POST",
        body: data
      });

      if (response.ok) {

        toast.success("Application submitted successfully!");

        setTimeout(() => {
          navigate("/career");
        }, 1500);

      } else {

        toast.error("Something went wrong");

      }

    } catch (error) {

      toast.error("Server error. Please try again.");

    }

  };

  return (
    <>
      <Header />

      <main className="bg-[#F5F6FA] min-h-screen">

        {/* Back Button */}

        <div className="max-w-5xl mx-auto px-6 pt-10">
          <button
            onClick={() => navigate("/career#openings")}
            className="text-[#1F2E4D] font-semibold hover:text-[#F4B400]"
          >
            ← Back to all openings
          </button>
        </div>


        {/* Page Title */}

        <section className="text-center py-10">

          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl font-bold text-[#1F2E4D]"
          >
            Apply for this job
          </motion.h1>

        </section>


        {/* Form */}

        <section className="pb-20">

          <div className="max-w-5xl mx-auto px-6">

            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-xl shadow-lg p-10 space-y-8"
            >

              {/* Resume Upload */}

              <div>

                <h2 className="text-xl font-semibold text-[#1F2E4D] mb-4">
                  Upload Resume *
                </h2>

                <input
                  type="file"
                  required
                  onChange={handleFileChange}
                  className="w-full border rounded-lg p-4"
                />

                <p className="text-sm text-gray-500 mt-2">
                  Upload PDF / DOC / DOCX. Max 10MB.
                </p>

              </div>


              {/* Personal Details */}

              <div className="grid md:grid-cols-2 gap-6">

                <div>
                  <label className="font-medium">First Name *</label>
                  <input
                    name="first_name"
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3 mt-2"
                  />
                </div>

                <div>
                  <label className="font-medium">Last Name *</label>
                  <input
                    name="last_name"
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3 mt-2"
                  />
                </div>

                <div>
                  <label className="font-medium">Email *</label>
                  <input
                    type="email"
                    name="email"
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3 mt-2"
                  />
                </div>

                <div>
                  <label className="font-medium">Mobile Phone *</label>
                  <input
                    name="phone"
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3 mt-2"
                  />
                </div>

              </div>


              {/* Experience */}

              <div className="grid md:grid-cols-2 gap-6">

                <div>
                  <label className="font-medium">Experience (Years)</label>
                  <input
                    type="number"
                    name="experience"
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3 mt-2"
                  />
                </div>

                <div>
                  <label className="font-medium">Available to Join (Days)</label>
                  <input
                    type="number"
                    name="available_to_join"
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3 mt-2"
                  />
                </div>

                <div>
                  <label className="font-medium">Current Salary</label>
                  <input
                    name="current_salary"
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3 mt-2"
                  />
                </div>

                <div>
                  <label className="font-medium">Expected Salary</label>
                  <input
                    name="expected_salary"
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3 mt-2"
                  />
                </div>

              </div>


              {/* Location */}

              <div>

                <label className="font-medium">Location</label>

                <input
                  name="location"
                  onChange={handleChange}
                  className="w-full border rounded-lg p-3 mt-2"
                />

              </div>


              {/* Submit Button */}

              <motion.button
                onClick={handleSubmit}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-gradient-to-r from-[#F4B400] to-[#F6C34A] text-black font-bold px-10 py-4 rounded-lg shadow"
              >
                Submit Application
              </motion.button>

            </motion.div>

          </div>

        </section>

      </main>

      <Footer />
    </>
  );
};

export default ApplyJob;