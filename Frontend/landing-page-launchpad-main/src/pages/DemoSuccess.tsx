import { motion } from "framer-motion";
import { CheckCircle2, Calendar, ArrowRight, PhoneCall, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SEO from "@/components/SEO";

const DemoSuccess = () => {
  const navigate = useNavigate();

  return (
    <>
      <SEO title="Demo Request Submitted" description="Your demo request for AI-Setu ERP has been submitted successfully. We'll be in touch soon!" />
      <Header />

      <main className="min-h-[80vh] flex items-center justify-center bg-gradient-to-b from-white to-[#F6F8FB] px-6 py-20">

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl w-full bg-white rounded-3xl shadow-xl border border-gray-100 p-10 md:p-14 text-center relative overflow-hidden"
        >

          {/* top gradient line */}
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-[#F4B400] via-[#FFD84D] to-[#E6B800]" />

          {/* success icon */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 180 }}
            className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-8"
          >
            <CheckCircle2 className="w-14 h-14 text-green-600" />
          </motion.div>

          {/* heading */}
          <h1 className="text-4xl md:text-5xl font-bold text-[#1F2E4D] mb-4">
            Demo Request Submitted 🎉
          </h1>

          {/* description */}
          <p className="text-lg text-gray-600 mb-12 leading-relaxed max-w-xl mx-auto">
            Thank you for your interest in <span className="font-bold text-[#F4B400]">AI-Setu ERP</span>.  
            Our product expert will contact you shortly to schedule your 
            <span className="font-semibold text-[#1F2E4D]"> personalized demo.</span>
          </p>

          {/* info cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12 text-left">

            <motion.div
              whileHover={{ y: -4 }}
              className="p-5 bg-blue-50 rounded-2xl flex items-start gap-3"
            >
              <PhoneCall className="w-5 h-5 text-blue-600 mt-1" />
              <div>
                <h3 className="font-semibold text-[#1F2E4D] text-sm">
                  Priority Callback
                </h3>
                <p className="text-xs text-gray-500">
                  Our expert will call you soon.
                </p>
              </div>
            </motion.div>

            <motion.div
              whileHover={{ y: -4 }}
              className="p-5 bg-purple-50 rounded-2xl flex items-start gap-3"
            >
              <Calendar className="w-5 h-5 text-purple-600 mt-1" />
              <div>
                <h3 className="font-semibold text-[#1F2E4D] text-sm">
                  Personalized Demo
                </h3>
                <p className="text-xs text-gray-500">
                  Tailored to your store type.
                </p>
              </div>
            </motion.div>

            <motion.div
              whileHover={{ y: -4 }}
              className="p-5 bg-green-50 rounded-2xl flex items-start gap-3"
            >
              <Clock className="w-5 h-5 text-green-600 mt-1" />
              <div>
                <h3 className="font-semibold text-[#1F2E4D] text-sm">
                  Within 24 Hours
                </h3>
                <p className="text-xs text-gray-500">
                  Expect our call shortly.
                </p>
              </div>
            </motion.div>

          </div>

          {/* buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">

            <Button
              onClick={() => navigate("/")}
              className="bg-[#1F2E4D] hover:bg-[#2D3748] text-white px-8 h-12 rounded-xl"
            >
              Back to Home
            </Button>

          </div>

          {/* small note */}
          <p className="text-xs text-gray-400 mt-8">
            Need immediate help? Call our support team anytime.
          </p>

        </motion.div>

      </main>

      <Footer />
    </>
  );
};

export default DemoSuccess;