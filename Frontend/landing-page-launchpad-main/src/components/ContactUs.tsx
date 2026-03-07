import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";

interface ContactFormData {
  name: string;
  phone: string;
  email: string;
  officeAddress: string;
  message: string;
}

export const submitContactForm = async (data: any) => {
  const response = await fetch("http://127.0.0.1:8000/api/contact/submit/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch {
    return {};
  }
};

const ContactUsPage = () => {
  const [formData, setFormData] = useState<ContactFormData>({
    name: "",
    phone: "",
    email: "",
    officeAddress: "",
    message: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const res = await submitContactForm(formData);

      if (res.message) {
        toast.success(res.message);

        setFormData({
          name: "",
          phone: "",
          email: "",
          officeAddress: "",
          message: "",
        });
      } else {
        toast.error("Something went wrong");
      }
    } catch {
      toast.error("Server error");
    }
  };

  return (
    <>
      <Header />

      <main className="min-h-screen bg-gray-50 py-16">
        <div className="container mx-auto px-6 lg:px-20">
          <h1 className="text-4xl font-bold text-center mb-6">Contact Us</h1>

          <div className="grid lg:grid-cols-2 gap-12 items-start">

            <form
              onSubmit={handleSubmit}
              className="bg-white shadow-xl rounded-xl p-8 space-y-6"
            >
              <Input
                placeholder="Full Name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />

              <Input
                placeholder="Phone Number"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                required
              />

              <Input
                placeholder="Email Address"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />

              <Input
                placeholder="Office Address"
                name="officeAddress"
                value={formData.officeAddress}
                onChange={handleChange}
                required
              />

              <Textarea
                placeholder="Tell us about what you are looking for"
                name="message"
                value={formData.message}
                onChange={handleChange}
                required
              />

              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-yellow-400 to-yellow-600 text-white font-bold py-4"
              >
                Submit Request
              </Button>
            </form>

            <div>
              <h2 className="text-3xl font-semibold mb-4">Why Choose Us?</h2>
              <ul className="space-y-3">
                <li>✔ Experienced team</li>
                <li>✔ Customized solutions</li>
                <li>✔ Fast support</li>
                <li>✔ Affordable pricing</li>
              </ul>
            </div>

          </div>
        </div>
      </main>

      <Footer />
    </>
  );
};

export default ContactUsPage;