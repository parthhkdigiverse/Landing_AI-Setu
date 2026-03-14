import { useState, useEffect } from "react";
import axios from "axios";
import { ClipboardCopy } from "lucide-react";
import toast, { Toaster } from "react-hot-toast";
import { API_BASE_URL } from "@/services/api";

const ReferralPopup = ({ open, onClose }: { open: boolean; onClose: () => void }) => {
  const [mobile, setMobile] = useState("");
  const [referralCode, setReferralCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  // Reset state every time popup opens
  useEffect(() => {
    if (open) {
      setMobile("");
      setReferralCode("");
      setLoading(false);
      setCopied(false);
    }
  }, [open]);

  const submitMobile = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {

      const res = await axios.post(
        `${API_BASE_URL}/referral-check/`,
        { mobile_number: mobile }
      );

      setReferralCode(res.data.referral_code);
      toast.success("Referral code generated!");

    } catch (error: any) {

      if (error.response?.data?.error) {
        toast.error(error.response.data.error);
      } else {
        toast.error("Something went wrong");
      }

      console.error(error);
    }

    setLoading(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(referralCode);
    setCopied(true);
    toast.success("Referral code copied!");
    setTimeout(() => setCopied(false), 2000);
  };

  if (!open) return null;

  return (
    <>
      <Toaster position="top-right" reverseOrder={false} />
      <div className="fixed inset-0 flex items-center justify-center bg-black/40 z-50 p-4">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-sm w-full p-6 relative animate-fadeIn">
          
          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
          >
            ✕
          </button>

          {!referralCode ? (
            <>
              <h2 className="text-2xl font-bold text-center mb-4 text-gray-800 dark:text-gray-100">
                Join Referral Program
              </h2>
              <p className="text-center text-gray-500 dark:text-gray-300 mb-6 text-sm">
                Enter your mobile number to get your referral code
              </p>
              <form onSubmit={submitMobile} className="space-y-4">
                <input
                  type="text"
                  placeholder="Mobile Number"
                  value={mobile}
                  onChange={(e) => setMobile(e.target.value)}
                  className="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3
                             placeholder:text-gray-400 dark:placeholder:text-gray-400
                             text-black dark:text-black
                             focus:ring-2 focus:ring-gold-gradient focus:outline-none dark:bg-gray-100"
                  required
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600 text-black font-semibold py-3 rounded-lg hover:opacity-90 transition"
                >
                  {loading ? "Checking..." : "Get Referral Code"}
                </button>
              </form>
            </>
          ) : (
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-3 text-gray-800 dark:text-gray-100">
                Your Referral Code
              </h2>
              <p className="text-4xl font-extrabold text-yellow-500 mb-4">{referralCode}</p>
              <button
                onClick={copyToClipboard}
                className="flex items-center justify-center mx-auto gap-2 bg-yellow-500 hover:bg-yellow-600 text-black font-semibold px-6 py-2 rounded-lg transition"
              >
                <ClipboardCopy className="w-5 h-5" />
                {copied ? "Copied!" : "Copy Code"}
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default ReferralPopup;