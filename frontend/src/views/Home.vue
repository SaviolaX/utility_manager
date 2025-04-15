<template>
  <LoadingSpinner v-if="isLoading" />
  <div v-else class="home-container">
    <p v-if="error">{{ error }}</p>
    <div class="home-container-input-block">
      <div class="home-container-utility-input">
        <h2>Gas</h2>
        <p>Gas</p>
        <input type="number" v-model="gasInput" required />
        <p>Price, m3</p>
        <input type="number" v-model="gasPrice" required />
        <p>Gas distribution</p>
        <input type="number" v-model="gasDistribution" required />
      </div>
      <div class="home-container-utility-input">
        <h2>Electricity</h2>
        <div class="home-container-utility-electricity-block">
          <div class="home-container-utility-electricity">
            <p>T1</p>
            <input type="number" v-model="t1electricityInput" required />
            <p>T2</p>
            <input type="number" v-model="t2electricityInput" required />
          </div>
          <div class="home-container-utility-electricity">
            <p>T1, Price/kw</p>
            <input type="number" v-model="t1electricityPrice" required />
            <p>T2, Price/kw</p>
            <input type="number" v-model="t2electricityPrice" required />
          </div>
        </div>
      </div>
      <div class="home-container-utility-input">
        <h2>Heat</h2>
        <p>Price</p>
        <input type="number" v-model="heatPrice" required />
        <p>Service</p>
        <input type="number" v-model="heatServicePrice" required />
      </div>
      <div class="home-container-utility-input">
        <h2>Water</h2>
        <div class="home-container-utility-water-block">
          <div class="home-container-utility-water">
            <p>Cold, Kitchen</p>
            <input type="number" v-model="waterInput.kitchen.cold" required />
            <p>Hot, Kitchen</p>
            <input type="number" v-model="waterInput.kitchen.hot" required />
          </div>
          <div class="home-container-utility-water">
            <p>Cold, Bathroom</p>
            <input type="number" v-model="waterInput.bathroom.cold" required />
            <p>Hot, Bathroom</p>
            <input type="number" v-model="waterInput.bathroom.hot" required />
          </div>
          <div class="home-container-utility-water">
            <p>Cold, Price</p>
            <input type="number" v-model="waterColdPrice" required />
            <p>Hot, Price</p>
            <input type="number" v-model="waterHotPrice" required />
          </div>
        </div>
      </div>
      <div class="home-container-utility-input">
        <h2>Utilities</h2>
        <p>Housing maintenance</p>
        <input type="number" v-model="housingMaintenance" required />
        <p>Garbage collection</p>
        <input type="number" v-model="garbageCollection" required />
      </div>
    </div>
    <div class="home-container-submit-button">
      <button @click="sendData">Submit</button>
    </div>
    <div v-if="showResultBlock" class="home-container-result-block">
      <div class="show-result-button-block">
        <button
          @click="closeResultBlock"
          class="close-show-result-block-button"
        >
          X
        </button>
      </div>
      <div v-if="objectDetails" style="display: flex">
        <table>
          <thead>
            <tr>
              <th></th>
              <th>Category</th>
              <th>New input</th>
              <th>Previous input</th>
              <th>Consumption</th>
              <th>Price/unit</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Gas</td>
              <td></td>
              <td>{{ objectDetails.utilities.gas.current }}</td>
              <td>{{ objectDetails.utilities.gas.previous }}</td>
              <td>{{ objectDetails.utilities.gas.consumption }}</td>
              <td>{{ objectDetails.prices.gas }}</td>
              <td>{{ objectDetails.cost.gas }}</td>
            </tr>
            <tr>
              <td></td>
              <td>Gas distribution</td>
              <td></td>
              <td></td>
              <td></td>
              <td>{{ objectDetails.prices.gas_distribution }}</td>
              <td>{{ objectDetails.prices.gas_distribution }}</td>
            </tr>
            <tr>
              <td>Water</td>
              <td>Cold kitchen</td>
              <td>{{ objectDetails.utilities.water.cold.kitchen.current }}</td>
              <td>{{ objectDetails.utilities.water.cold.kitchen.previous }}</td>
              <td>
                {{ objectDetails.utilities.water.cold.kitchen.consumption }}
              </td>
              <td>{{ objectDetails.prices.water.cold }}</td>
              <td>{{ objectDetails.cost.water.kitchen_cold }}</td>
            </tr>
            <tr>
              <td></td>
              <td>Cold bathroom</td>
              <td>{{ objectDetails.utilities.water.cold.bathroom.current }}</td>
              <td>
                {{ objectDetails.utilities.water.cold.bathroom.previous }}
              </td>
              <td>
                {{ objectDetails.utilities.water.cold.bathroom.consumption }}
              </td>
              <td>{{ objectDetails.prices.water.cold }}</td>
              <td>{{ objectDetails.cost.water.bathroom_cold }}</td>
            </tr>
            <tr>
              <td></td>
              <td>Hot kitchen</td>
              <td>{{ objectDetails.utilities.water.hot.kitchen.current }}</td>
              <td>
                {{ objectDetails.utilities.water.hot.kitchen.previous }}
              </td>
              <td>
                {{ objectDetails.utilities.water.hot.kitchen.consumption }}
              </td>
              <td>{{ objectDetails.prices.water.hot }}</td>
              <td>{{ objectDetails.cost.water.kitchen_hot }}</td>
            </tr>
            <tr>
              <td></td>
              <td>Hot bathroom</td>
              <td>{{ objectDetails.utilities.water.hot.bathroom.current }}</td>
              <td>
                {{ objectDetails.utilities.water.hot.bathroom.previous }}
              </td>
              <td>
                {{ objectDetails.utilities.water.hot.bathroom.consumption }}
              </td>
              <td>{{ objectDetails.prices.water.hot }}</td>
              <td>{{ objectDetails.cost.water.bathroom_hot }}</td>
            </tr>
            <tr>
              <td>Electricity</td>
              <td>T1</td>
              <td>{{ objectDetails.utilities.electricity.t1.current }}</td>
              <td>{{ objectDetails.utilities.electricity.t1.previous }}</td>
              <td>
                {{ objectDetails.utilities.electricity.t1.consumption }}
              </td>
              <td>{{ objectDetails.prices.electricity.t1 }}</td>
              <td>{{ objectDetails.cost.electricity.t1 }}</td>
            </tr>
            <tr>
              <td></td>
              <td>T2</td>
              <td>{{ objectDetails.utilities.electricity.t2.current }}</td>
              <td>{{ objectDetails.utilities.electricity.t2.previous }}</td>
              <td>
                {{ objectDetails.utilities.electricity.t2.consumption }}
              </td>
              <td>{{ objectDetails.prices.electricity.t2 }}</td>
              <td>{{ objectDetails.cost.electricity.t2 }}</td>
            </tr>
            <tr>
              <td>Heat</td>
              <td>Hot water</td>
              <td>{{ objectDetails.utilities.heat.current }}</td>
              <td>{{ objectDetails.utilities.heat.previous }}</td>
              <td>{{ objectDetails.utilities.heat.consumption }}</td>
              <td>{{ objectDetails.prices.heat }}</td>
              <td>{{ objectDetails.cost.heat }}</td>
            </tr>
            <tr>
              <td></td>
              <td>Heat service</td>
              <td></td>
              <td></td>
              <td></td>
              <td>{{ objectDetails.prices.heat_service }}</td>
              <td>{{ objectDetails.prices.heat_service }}</td>
            </tr>
            <tr>
              <td>Services</td>
              <td>Garbage</td>
              <td></td>
              <td></td>
              <td></td>
              <td>{{ objectDetails.prices.garbage }}</td>
              <td>{{ objectDetails.prices.garbage }}</td>
            </tr>
            <tr>
              <td></td>
              <td>Housing</td>
              <td></td>
              <td></td>
              <td></td>
              <td>{{ objectDetails.prices.housing }}</td>
              <td>{{ objectDetails.prices.housing }}</td>
            </tr>
            <tr>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td>Total cost:</td>
              <td>{{ objectDetails.cost.total_cost }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="home-container-history-block">
      <div
        v-for="utility in utilitiesList"
        :key="utility"
        class="history-utility-card"
        @click="getObjectResult(utility.date)"
      >
        <p>Date: {{ utility.formattedDate }}</p>
        <p v-if="utility.cost.total_cost !== '?'">
          Total cost: {{ utility.cost.total_cost }}
        </p>
        <p v-else>first record</p>
      </div>
    </div>
  </div>
</template>

<script>
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import { dateToString, sortByDate } from "@/services/main";
import { useAuthStore } from "@/stores/auth";
import { fetchAuthSession } from "aws-amplify/auth";
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "Home",
  components: {
    LoadingSpinner,
  },

  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const COUNT_URL =
      "https://rtem6et0wh.execute-api.eu-central-1.amazonaws.com/dev/count";

    const error = ref(null);

    const utilitiesList = ref(null);

    // Input
    const gasInput = ref(null);
    const waterInput = ref({
      kitchen: { cold: null, hot: null },
      bathroom: { cold: null, hot: null },
    });
    const electricityInput = ref(null);
    const t1electricityInput = ref(null);
    const t2electricityInput = ref(null);

    // Prices
    const gasPrice = ref(null);
    const gasDistribution = ref(null);
    const waterColdPrice = ref(null);
    const waterHotPrice = ref(null);
    const electricityPrice = ref(null);
    const t1electricityPrice = ref(null);
    const t2electricityPrice = ref(null);
    const garbageCollection = ref(null);
    const housingMaintenance = ref(null);
    const heatServicePrice = ref(null);
    const heatPrice = ref(null);

    const objectDetails = ref(null);
    const showResultBlock = ref(false);
    const isLoading = ref(true);

    onMounted(async () => {
      try {
        await getCurrentSession();
        await getData();
      } catch (err) {
        console.log("Error in mounted:", err);
      } finally {
        isLoading.value = false;
      }
    });

    const getCurrentSession = async () => {
      try {
        const session = await fetchAuthSession();

        if (session) {
          await setUserSession(session);
        }
      } catch (err) {
        redirectToSignIn();
        console.log("No user on mounted in Home.");
      }
    };
    const setUserSession = async (session) => {
      authStore.setUser({
        user: {
          username: session.userSub,
          email: session.tokens.signInDetails?.loginId,
        },
        isLoggedIn: true,
        authToken: session.tokens.idToken.toString(),
      });
    };
    const redirectToSignIn = () => {
      router.push("/signin");
    };
    const getData = async () => {
      try {
        const resp = await fetch(COUNT_URL, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.authToken}`,
          },
        });
        const data = await resp.json();
        if (resp.status !== 200) {
          console.log("Server side error: ", data.error);
          utilitiesList.value = [];
          error.value = "Bad request error.";
        } else {
          utilitiesList.value = sortByDate(data.utilities_list, "desc");
          console.log(utilitiesList.value);
        }
      } catch (error) {
        console.log("GET request error: ", error);
      }
    };
    const sendData = async () => {
      const payload = {
        date: dateToString(),
        utilities: {
          gas: gasInput.value,
          electricity: {
            t1: t1electricityInput.value,
            t2: t2electricityInput.value,
          },
          water: {
            cold: {
              kitchen: waterInput.value.kitchen.cold,
              bathroom: waterInput.value.bathroom.cold,
            },
            hot: {
              kitchen: waterInput.value.kitchen.hot,
              bathroom: waterInput.value.bathroom.hot,
            },
          },
        },
        prices: {
          gas: gasPrice.value,
          gas_distribution: gasDistribution.value,
          electricity: {
            t1: t1electricityPrice.value,
            t2: t2electricityPrice.value,
          },
          water: {
            cold: waterColdPrice.value,
            hot: waterHotPrice.value,
          },
          housing: housingMaintenance.value,
          garbage: garbageCollection.value,
          heat_service: heatServicePrice.value,
          heat_price: heatPrice.value,
        },
      };
      console.log("Submitted data:", payload);
      try {
        const response = await fetch(COUNT_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.authToken}`,
          },
          body: JSON.stringify({
            body: { payload },
          }),
        });
        const data = await response.json();
        console.log(data);
        if (response.status !== 200) {
          console.log("Server side error: ", data.error);
          error.value = "Bad request error.";
        } else {
          console.log("POST -> Response from server:", data);
          showResultBlock.value = false;
          await getData();
          // remove input values
          cleanInputs();
        }
      } catch (error) {
        console.log("POST request error: ", error);
      }
    };
    const cleanInputs = () => {
      gasInput.value = null;
      waterInput.value = {
        kitchen: { cold: null, hot: null },
        bathroom: { cold: null, hot: null },
      };
      t1electricityInput.value = null;
      t2electricityInput.value = null;
      electricityInput.value = null;
    };

    const getObjectResult = (date) => {
      objectDetails.value = utilitiesList.value.find(
        (object) => object.date === date
      );
      console.log("Object details:", objectDetails.value);
      showResultBlock.value = true;
    };
    const closeResultBlock = () => {
      showResultBlock.value = false;
    };

    // Observes for price changes and put ones into input fields.
    watch(utilitiesList, (newValue) => {
      if (newValue.length !== 0) {
        const sortedData = sortByDate(newValue, "desc");
        const lastObjByDate = sortedData[0];
        gasPrice.value = lastObjByDate.prices.gas;
        gasDistribution.value = lastObjByDate.prices.gas_distribution;
        t1electricityPrice.value = lastObjByDate.prices.electricity.t1;
        t2electricityPrice.value = lastObjByDate.prices.electricity.t2;
        waterColdPrice.value = lastObjByDate.prices.water.cold;
        waterHotPrice.value = lastObjByDate.prices.water.hot;
        heatPrice.value = lastObjByDate.prices.heat;
        heatServicePrice.value = lastObjByDate.prices.heat_service;
        housingMaintenance.value = lastObjByDate.prices.housing;
        garbageCollection.value = lastObjByDate.prices.garbage;
      }
    });

    return {
      // API request
      sendData,
      // Inputs
      waterInput,
      gasInput,
      t1electricityInput,
      t2electricityInput,
      electricityInput,
      // Prices
      gasPrice,
      gasDistribution,
      waterColdPrice,
      waterHotPrice,
      electricityPrice,
      t1electricityPrice,
      t2electricityPrice,
      heatServicePrice,
      garbageCollection,
      housingMaintenance,
      heatPrice,
      // Data
      objectDetails,
      utilitiesList,
      getObjectResult,
      // Functions
      closeResultBlock,
      // Other
      isLoading,
      showResultBlock,
      error,
    };
  },
};
</script>

<style>
.home-container {
  display: flex;
  flex-direction: column; /* Stack children vertically */
  align-items: center; /* Center horizontally */
  gap: 20px; /* Space between input block and button */
}
.home-container-input-block {
  display: flex;
  align-items: flex-start; /* Crucial for top alignment */
  gap: 20px; /* Better spacing between sections */
  justify-content: center;
}

.home-container-utility-input {
  margin: 10px 0; /* Adjust as needed */
}

.home-container-utility-input h2,
.home-container-utility-input p {
  color: #d1d5db;
  margin: 0 0 5px 0; /* Reset margins */
}

.home-container-utility-water-block {
  display: flex;
  gap: 10px; /* Consistent spacing */
}
.home-container-utility-electricity-block {
  display: flex;
  gap: 10px; /* Consistent spacing */
}
.home-container-submit-button {
  /* Optional: Add margin-top if more spacing is needed */
  margin-top: 20px;
}

.home-container-submit-button button {
  padding: 10px 20px; /* Better button size */
  background: #3b82f6; /* Example blue color */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.home-container-submit-button button:hover {
  background: #2563eb; /* Darker blue on hover */
}
/* Remove arrows for all number inputs */
input[type="number"] {
  appearance: textfield; /* Standard */
  -moz-appearance: textfield; /* Firefox */
}

/* Remove arrows in Chrome/Safari */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.home-container-history-block {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.history-utility-card {
  margin: 10px;
  padding: 10px;
  background: #374151;
  color: #d1d5db;
  border-radius: 10px;
}
.history-utility-card:hover {
  border: 1px solid #d1d5db;
  transition: border 0.6s ease, background-color 0.6s ease;
}

.home-container-result-block {
  display: flex;
  flex-direction: column;
  color: #d1d5db;
  gap: 20px;
  background-color: #374151; /* Dark Theme: Medium-dark gray */
  padding: 35px;
  border-radius: 8px;
  margin-top: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow for dark bg */
  position: relative;
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
/* Table styling */
table {
  width: 100%;
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
</style>
