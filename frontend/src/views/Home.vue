<template>
  <div class="home-container">
    <div class="home-container-input-block">
      <table>
        <thead>
          <tr>
            <th>Gas</th>
            <th>Gas Price</th>
            <th>Gas Distribution</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                type="number"
                placeholder="Gas numbers"
                v-model="gasInput"
              />
            </td>
            <td>
              <input type="number" placeholder="$/m3" v-model="gasPrice" />
            </td>
            <td>
              <input type="number" placeholder="$" v-model="gasDistribution" />
            </td>
          </tr>
        </tbody>
      </table>
      <table>
        <thead>
          <tr>
            <th>Heat</th>
            <th>Heat Price</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                type="number"
                placeholder="Heat numbers"
                v-model="heatInput"
              />
            </td>
            <td>
              <input type="number" placeholder="$/m3" v-model="heatPrice" />
            </td>
          </tr>
        </tbody>
      </table>
      <table>
        <thead>
          <tr>
            <th>Electricity</th>
            <th>Electricity Price</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                type="number"
                placeholder="T1"
                v-model="t1electricityInput"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="$/kw"
                v-model="t1electricityPrice"
              />
            </td>
          </tr>
          <tr>
            <td>
              <input
                type="number"
                placeholder="T2"
                v-model="t2electricityInput"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="$/kw"
                v-model="t2electricityPrice"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <table>
        <thead>
          <tr>
            <th>Kitchen</th>
            <th>Bathroom</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                type="number"
                placeholder="Cold. Kitchen"
                v-model="waterInput.kitchen.cold"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="Cold. Bathroom"
                v-model="waterInput.bathroom.cold"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="Price, m3"
                v-model="waterColdPrice"
              />
            </td>
          </tr>
          <tr>
            <td>
              <input
                type="number"
                placeholder="Hot. Kitchen"
                v-model="waterInput.kitchen.hot"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="Hot. Bathroom"
                v-model="waterInput.bathroom.hot"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="Price, m3"
                v-model="waterHotPrice"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="sendInputData">Submit</button>
    </div>
    <div v-if="showResultBlock" class="home-container-result-block">
      <div class="show-result-button-block">
        <button @click="closeResultBlock" class="close-show-result-block-button">X</button>
      </div>
      <p v-if="objectDetails">{{ objectDetails }}</p>
    </div>
    <div class="home-container-history-block">
      <div v-for="object in mockData" :key="object" class="history-object">
        <button @click="getObjectResult(object.id)">{{ object.date }}</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { fetchAuthSession } from "aws-amplify/auth";
import { ref } from "vue";

export default {
  name: "Home",

  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const COUNT_URL =
      "https://a8lx65txd8.execute-api.eu-central-1.amazonaws.com/dev/count";

    const mockData = [
      {
        id: 1,
        date: "22.03.2025",
        body: {
          gas: {
            input: 100,
            price: 1.5,
            distribution: 0.5,
          },
          heat: {
            input: 200,
            price: 2.0,
          },
          electricity: {
            t1Input: 300,
            t1Price: 0.3,
            t2Input: 400,
            t2Price: 0.4,
          },
          water: {
            kitchen: {
              coldInput: 50,
              hotInput: 60,
              coldPrice: 0.2,
              hotPrice: 0.3,
            },
            bathroom: {
              coldInput: 70,
              hotInput: 80,
              coldPrice: 0.25,
              hotPrice: 0.35,
            },
          },
        },
      },
      {
        id: 2,
        date: "22.02.2025",
        body: {
          gas: {
            input: 110,
            price: 1.6,
            distribution: 0.6,
          },
          heat: {
            input: 210,
            price: 2.1,
          },
          electricity: {
            t1Input: 310,
            t1Price: 0.31,
            t2Input: 410,
            t2Price: 0.41,
          },
          water: {
            kitchen: {
              coldInput: 55,
              hotInput: 65,
              coldPrice: 0.22,
              hotPrice: 0.32,
            },
            bathroom: {
              coldInput: 75,
              hotInput: 85,
              coldPrice: 0.27,
              hotPrice: 0.37,
            },
          },
        },
      },
    ];
    const gasInput = ref(null);
    const gasPrice = ref(null);
    const gasDistribution = ref(null);
    const waterInput = ref({
      kitchen: { cold: null, hot: null },
      bathroom: { cold: null, hot: null },
    });
    const waterColdPrice = ref(null);
    const waterHotPrice = ref(null);
    const heatInput = ref(null);
    const heatPrice = ref(null);
    const electricityInput = ref(null);
    const electricityPrice = ref(null);
    const t1electricityInput = ref(null);
    const t1electricityPrice = ref(null);
    const t2electricityInput = ref(null);
    const t2electricityPrice = ref(null);

    const objectDetails = ref(null);
    const showResultBlock = ref(false);

    return {
      authStore,
      router,
      COUNT_URL,
      waterInput,
      gasInput,
      gasPrice,
      gasDistribution,
      waterColdPrice,
      waterHotPrice,
      heatInput,
      heatPrice,
      electricityInput,
      electricityPrice,
      t1electricityInput,
      t1electricityPrice,
      t2electricityInput,
      t2electricityPrice,
      mockData,
      objectDetails,
      showResultBlock,
    };
  },
  //TODO: to think abot getCurrentUser and fetchAuthSession
  async mounted() {
    try {
      const session = await fetchAuthSession();

      if (session) {
        this.authStore.setUser({
          user: {
            username: session.userSub,
            email: session.tokens.signInDetails?.loginId,
          },
          isLoggedIn: true,
          authToken: session.tokens.idToken.toString(),
        });
      }
    } catch (err) {
      this.router.push("/signin");
      console.log("No user on mounted in Home.");
    }
  },
  methods: {
    async sendInputData() {
      // This method will handle the submission of input data
      const inputData = {
        gasInput: this.gasInput,
        gasPrice: this.gasPrice,
        gasDistribution: this.gasDistribution,
        waterInput: this.waterInput,
        waterColdPrice: this.waterColdPrice,
        waterHotPrice: this.waterHotPrice,
        heatInput: this.heatInput,
        heatPrice: this.heatPrice,
        electricityInput: this.electricityInput,
        electricityPrice: this.electricityPrice,
        t1electricityInput: this.t1electricityInput,
        t1electricityPrice: this.t1electricityPrice,
        t2electricityInput: this.t2electricityInput,
        t2electricityPrice: this.t2electricityPrice,
      };
      console.log("Submitted data:", inputData);
      const response = await fetch(this.COUNT_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.authStore.authToken}`,
        },
        body: JSON.stringify(inputData),
      });
      const data = await response.json();
      this.resp = data;
      console.log("Response from server:", data);
    },
    async getReq() {
      const resp = await fetch(this.COUNT_URL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.authStore.authToken}`,
        },
      });
      const data = await resp.json();
      this.resp = JSON.parse(data.body);
      console.log("Response from server:", this.resp);
    },
    getObjectResult(id) {
      this.objectDetails = this.mockData.find((object) => object.id === id);
      this.showResultBlock = true;
    },
    closeResultBlock() {
      this.showResultBlock = false;
    },
  },
};
</script>

<style>
/* Style the main container */
.home-container {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding: 20px;
  background-color: #1f2937; /* Dark Theme: Dark slate gray background */
  color: #d1d5db; /* Dark Theme: Light gray default text color */
}

/* Style the input block containing all tables */
.home-container-input-block {
  display: flex;
  gap: 20px;
  background-color: #374151; /* Dark Theme: Medium-dark gray */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow for dark bg */
}
.home-container-result-block {
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: #374151; /* Dark Theme: Medium-dark gray */
  padding: 20px;
  border-radius: 8px;
  margin-top: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow for dark bg */
  position: relative;
}
/* Container for history objects */
.home-container-history-block {
  display: flex;
  flex-wrap: wrap; /* ADDED: Allows items to wrap onto multiple lines */
  justify-content: flex-start; /* CHANGED: Aligns items to the start of each line */
  gap: 20px; /* Keeps consistent spacing between items, both horizontally and vertically */
  padding: 20px;
  border-radius: 8px;
  margin: 0 10px; /* Existing margin */
  margin-top: 1.5rem; /* Existing margin */
  /* You might want to ensure this container has a background matching the theme */
  /* e.g., background-color: #374151; */
}

/* Individual history object styling (remains the same) */
.history-object {
  background-color: #4b5563; /* Dark Theme: Slightly lighter gray for history objects */
  padding: 10px;
  border-radius: 8px;
  color: #f9fafb; /* Dark Theme: Very light gray/white text for contrast */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow */
  /* Optional: You might want to add a min-width or width to history objects */
  /* E.g., min-width: 100px; */
}

/* Table styling */
table {
  width: 100%;
  max-width: 600px;
  border-collapse: collapse;
  background-color: #2d3748; /* Dark Theme: Slightly darker gray for table */
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow */
  overflow: hidden;
}

/* Table header styling */
thead th {
  background-color: #4b5563; /* Dark Theme: Slightly lighter gray for headers */
  color: #f9fafb; /* Dark Theme: Very light gray/white text for contrast */
  padding: 10px;
  text-align: left;
  font-weight: 600;
}

/* Table body styling */
tbody td {
  padding: 10px;
  border-bottom: 1px solid #4b5563; /* Dark Theme: Medium gray border */
  color: #d1d5db; /* Dark Theme: Light gray text */
}

/* Input styling */
input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #4b5563; /* Dark Theme: Medium gray border */
  border-radius: 4px;
  font-size: 14px;
  background-color: #1f2937; /* Dark Theme: Dark background for input */
  color: #e5e7eb; /* Dark Theme: Lighter text for input */
  transition: border-color 0.3s ease;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

/* Remove arrows specifically for Firefox */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox fallback */
input[type="number"] {
  appearance: textfield;
  -moz-appearance: textfield;
}

input[type="number"]:focus {
  border-color: #60a5fa; /* Soft blue for focus (often okay on dark) */
  outline: none;
  box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.3); /* Dark Theme: Slightly more opaque focus ring */
}

/* Placeholder text styling */
input::placeholder {
  color: #6b7280; /* Dark Theme: Dimmer gray for placeholder */
  font-style: italic;
}

/* Hover effect for table rows */
tbody tr:hover {
  background-color: #212831; /* Dark Theme: Slightly lighter gray for hover */
}

/* Button styling */
.home-container-input-block button {
  background-color: #3b82f6; /* Clean blue (usually contrasts well) */
  color: #ffffff; /* White text */
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.home-container-input-block button:hover {
  background-color: #2563eb; /* Slightly darker blue on hover */
}

.show-result-button-block {
  position: absolute; /* Takes the button out of normal document flow */
  top: 0;
  right: 0;
  padding: 5px; /* Optional: adds some space around the button */
}

.close-show-result-block-button {
  background: none;
  border: 1px solid #4b5563; /* Dark Theme: Medium gray border */
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  padding: 5px 10px; /* Adjust padding as needed */
  /* Optional styling to make the button more visible */
  color: #ffff;
  font-weight: bold;
}

.close-show-result-block-button:hover {
  color: #ffff; /* Optional hover effect */
  background-color: #4b5563; /* Dark Theme: Medium gray background */
  border: 1px solid #f7537c; /* Clean blue border */
}

/* Responsive adjustments (no color changes needed here) */
@media (max-width: 768px) {
  .home-container-input-block {
    gap: 15px;
  }

  table {
    max-width: 100%;
  }

  input[type="number"] {
    font-size: 12px;
    padding: 6px;
  }
}
</style>
