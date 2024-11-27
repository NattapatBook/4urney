<template>
  <v-app>
    <!-- layout -->
    <div
      :style="{
        boxShadow:
          scrollPosition > 60
            ? `1px 2px ${
                scrollPosition - 60 > 20 ? 20 : scrollPosition - 60
              }px 0px black !important`
            : ``,
      }"
      class="landing-layout pa-4"
    >
      <div
        class="div-app-bar"
        :style="{ fontWeight: `bold`, cursor: `pointer` }"
        @click="scrollTo('landingPage')"
      >
        <v-avatar class="mr-2">
          <img :style="{ height: `50px` }" src="@/assets/img/4urneyLogo.png" />
        </v-avatar>
        <p :style="{ fontSize: `1.2rem` }">4urney</p>
      </div>
      <v-spacer></v-spacer>
      <v-btn
        v-if="windowWidth > 880"
        variant="text"
        @click="scrollTo('features')"
        >Features</v-btn
      >
      <!-- <v-btn
        v-if="windowWidth > 880"
        variant="text"
        @click="scrollTo('solution')"
        >Solution</v-btn
      > -->
      <v-btn
        v-if="windowWidth > 880"
        variant="text"
        @click="scrollTo('pricing')"
        >Pricing</v-btn
      >

      <v-dialog
        v-if="windowWidth > 880"
        max-width="500"
        transition="dialog-bottom-transition"
      >
        <template v-slot:activator="{ props: activatorProps }">
          <v-btn v-bind="activatorProps" variant="text">Contact Us</v-btn>
        </template>

        <template v-slot:default="{ isActive }">
          <v-card
            class="rounded-xl pa-4"
            :style="{ backgroundColor: `#f1f1f1` }"
          >
            <v-card-title class="card-title-contact-dialog">
              <span>Contact Us</span>
              <v-btn
                variant="plain"
                text
                icon="mdi-close"
                @click="isActive.value = false"
              ></v-btn>
            </v-card-title>
            <v-card-text>
              <div
                class="mb-5"
                :style="{ display: `flex`, justifyContent: `center` }"
              >
                <v-avatar :style="{ width: `150px`, height: `150px` }">
                  <v-img
                    src="https://itupdate.com.au/IBMPartnerSolutionsHub/images/Partner-logo-circle-4plus.png"
                  />
                </v-avatar>
              </div>
              <p :style="{ fontWeight: `bold` }">
                4Plus Group Company Limited.
              </p>
              <p>18th Floor K.S.L.Tower</p>
              <p>503 Sri-Ayutthaya Road, Ratchathewi</p>
              <p>Bangkok 10400, Thailand</p>
              <p>
                Emall.
                <span :style="{ fontWeight: `bold` }">4urney@4plus.co.th</span>
              </p>
              <p>
                Tel. <span :style="{ fontWeight: `bold` }">+662 640 1151</span>
              </p>
            </v-card-text>
          </v-card>
        </template>
      </v-dialog>
      <v-menu transition="fab-transition" class="rounded-xl">
        <template v-slot:activator="{ props }">
          <v-btn
            v-if="windowWidth <= 880"
            class="mr-2"
            icon="mdi-dots-vertical"
            variant="text"
            v-bind="props"
          ></v-btn>
        </template>

        <v-list class="pa-0 rounded-lg">
          <v-list-item class="pa-0">
            <v-card class="pa-4" @click="scrollTo('features')" elevation="0">
              <span>🚀 Features</span>
            </v-card>
          </v-list-item>
          <v-list-item class="pa-0">
            <v-card class="pa-4" @click="scrollTo('pricing')" elevation="0">
              <span>🏷️ Pricing</span>
            </v-card>
          </v-list-item>
          <!-- <v-list-item class="pa-0">
            <v-card class="pa-4" @click="scrollTo('solution')" elevation="0">
              <span>Solution</span>
            </v-card>
          </v-list-item> -->
          <!-- <v-list-item class="pa-0">
            <v-card
              class="pa-4"
              @click="scrollTo('trustedCustomers')"
              elevation="0"
            >
              <span>Our Trusted Customers</span>
            </v-card>
          </v-list-item> -->

          <v-list-item class="pa-0">
            <v-dialog max-width="500" transition="dialog-bottom-transition">
              <template v-slot:activator="{ props: activatorProps }">
                <v-card
                  v-bind="activatorProps"
                  class="pa-4"
                  @click="scrollTo('trustedCustomers')"
                  elevation="0"
                >
                  <span>📞 Contact Us</span>
                </v-card>
              </template>

              <template v-slot:default="{ isActive }">
                <v-card
                  elevation="0"
                  class="rounded-xl pa-4"
                  :style="{ backgroundColor: `#f1f1f1` }"
                >
                  <v-card-title class="card-title-contact-dialog">
                    <span>Contact Us</span>
                    <v-btn
                      variant="plain"
                      text
                      icon="mdi-close"
                      @click="isActive.value = false"
                    ></v-btn>
                  </v-card-title>
                  <v-card-text>
                    <div
                      class="mb-5"
                      :style="{ display: `flex`, justifyContent: `center` }"
                    >
                      <v-avatar :style="{ width: `150px`, height: `150px` }">
                        <v-img
                          src="https://itupdate.com.au/IBMPartnerSolutionsHub/images/Partner-logo-circle-4plus.png"
                        />
                      </v-avatar>
                    </div>
                    <p :style="{ fontWeight: `bold` }">
                      4Plus Group Company Limited.
                    </p>
                    <p>18th Floor K.S.L.Tower</p>
                    <p>503 Sri-Ayutthaya Road, Ratchathewi</p>
                    <p>Bangkok 10400, Thailand</p>
                    <p>
                      Emall.
                      <span :style="{ fontWeight: `bold` }"
                        >4urney@4plus.co.th</span
                      >
                    </p>
                    <p>
                      Tel.
                      <span :style="{ fontWeight: `bold` }">+662 640 1151</span>
                    </p>
                  </v-card-text>
                </v-card>
              </template>
            </v-dialog>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn
        class="get-login-btn rounded-lg px-5 py-2"
        color="primary"
        @click="$emit('navigate', 'home')"
        >Login</v-btn
      >
    </div>

    <v-main>
      <v-container fluid class="px-0">
        <!-- Landing Page Section -->
        <v-row
          justify="center"
          align="center"
          class="landing-page"
          id="landingPage"
          :style="{
            height: windowWidth > 960 ? `100vh` : `calc(100vh - 10vh)`,
          }"
        >
          <v-col cols="9" sm="9" md="8" lg="8" xl="6" xxl="6">
            <v-carousel
              class="rounded-xl"
              hide-delimiters
              hide-delimiter-background
              show-arrows="hover"
            >
              <!-- BOOST -->
              <v-carousel-item>
                <v-card class="pa-4 rounded-xl card-landing-top">
                  <v-card-title>
                    <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                      BOOST 🚀
                    </p>
                    <p :style="{ fontSize: `0.8em` }">Your Customer Service</p>
                    <p :style="{ fontSize: `0.8em` }">
                      with
                      <span
                        class="gradient-text"
                        :style="{ fontWeight: `bold` }"
                        >AI-Powered</span
                      >
                    </p>
                  </v-card-title>
                  <v-card-text class="pb-0">
                    <p :style="{ fontSize: `1rem`, color: `grey` }">
                      "Seamlessly integrate with LINE OA, Facebook, and more.
                      Manage chats effortlessly with automated responses and
                      personalized support to resolve customer issues quickly."
                    </p>
                  </v-card-text>
                  <v-card-text
                    :style="{
                      display: `flex`,
                      justifyContent: `center`,
                    }"
                  >
                    <div
                      :style="{
                        width: `100%`,
                        display: `flex`,
                        justifyContent: `center`,
                      }"
                    >
                      <img
                        :style="{
                          width: `100%`,
                          maxWidth: `700px`,
                          aspectRatio: '580 / 221',
                          objectFit: 'contain',
                        }"
                        src="@/assets/img/landing/showChat.png"
                      />
                    </div>

                    <!-- <div
                      class="mb-2"
                      v-for="(item, idx) in showChat"
                      :key="`landing_show_chat_${idx}`"
                      :style="{
                        display: `flex`,
                        justifyContent:
                          item.type === `customer` ? `flex-start` : `flex-end`,
                      }"
                    >
                      <v-avatar
                        v-if="item.type === `customer`"
                        size="small"
                        class="mr-2"
                      >
                        <v-img
                          :src="`https://ui-avatars.com/api/?name=${item.type}`"
                          aspect-ratio="1"
                        ></v-img>
                      </v-avatar>
                      <v-chip
                        :style="{
                          backgroundColor:
                            item.type === `admin`
                              ? `#8eff8e`
                              : item.type === `ai`
                              ? `rgba(242, 195, 235, 1)`
                              : ``,
                          color:
                            item.type === `ai` ? `rgba(254, 56, 147, 1)` : ``,
                        }"
                      >
                        {{ item.msg }}
                      </v-chip>
                      <v-avatar
                        v-if="item.type !== `customer`"
                        size="small"
                        class="ml-2"
                      >
                        <v-img
                          :src="`https://ui-avatars.com/api/?name=${item.type}`"
                          aspect-ratio="1"
                        ></v-img>
                      </v-avatar>
                    </div> -->
                  </v-card-text>
                </v-card>
              </v-carousel-item>
              <!-- CORE -->
              <v-carousel-item>
                <v-card class="pa-4 rounded-xl card-landing-top">
                  <v-card-title>
                    <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                      CORE 🌟
                    </p>
                  </v-card-title>
                  <v-card-text
                    class="pb-0"
                    :style="{ height: `calc(100% - 165px)`, overflowX: `auto` }"
                  >
                    <v-container>
                      <v-row>
                        <v-col
                          cols="12"
                          sm="12"
                          md="12"
                          lg="6"
                          xl="6"
                          xxl="6"
                          v-for="(item, idx) in core"
                          :key="`core_item_key=${idx}`"
                        >
                          <v-tooltip location="bottom">
                            <template v-slot:activator="{ props }">
                              <v-chip
                                v-bind="props"
                                class="mb-2 pr-4"
                                :style="{
                                  maxWidth: `100%`,
                                }"
                              >
                                <div
                                  :style="{
                                    display: `grid`,
                                  }"
                                >
                                  <span class="ellipsis-text">
                                    {{ item.emoji }}{{ item.head }}</span
                                  >
                                </div>
                              </v-chip>
                            </template>
                            <span>{{ item.head }}</span>
                          </v-tooltip>
                          <p class="ml-2">{{ item.body }}</p>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>
                </v-card>
              </v-carousel-item>
              <!-- login&trial both in > 880 -->
              <v-carousel-item v-if="windowWidth > 880">
                <v-card
                  :style="{
                    height: `100%`,
                    display: `flex`,
                    justifyContent: `space-between`,
                  }"
                >
                  <!-- login -->
                  <v-card
                    elevation="0"
                    class="pa-4 rounded-xl card-landing-top"
                    :style="{ height: `100%`, width: `50%` }"
                  >
                    <v-card-title>
                      <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                        Login 🔑
                      </p>
                      <p :style="{ fontSize: `0.8em` }">"Start Your Journey"</p>
                      <p :style="{ fontSize: `0.8em` }">
                        &nbsp;Smarter, faster, easier service.
                      </p>
                      <p :style="{ fontSize: `0.8em` }">
                        &nbsp;with the
                        <span
                          class="gradient-text"
                          :style="{ fontWeight: `bold` }"
                          >Power of AI</span
                        >.
                      </p>
                    </v-card-title>
                    <v-card-text
                      class="pb-0"
                      :style="{
                        height: `calc(100% - 64px)`,
                        overflowX: `auto`,
                        display: `flex`,
                        alignItems: `center`,
                        flexDirection: `column`,
                        justifyContent: `flex-start`,
                      }"
                    >
                      <p
                        class="mb-10 mt-5"
                        :style="{ color: `grey`, textAlign: `center` }"
                      >
                        Log In to Begin Experience AI Power
                      </p>
                      <v-btn
                        class="get-login-page-btn rounded-lg"
                        color="primary"
                        elevation="10"
                        :style="{ width: `15em` }"
                      >
                        Login
                      </v-btn>

                      <p
                        class="mt-10"
                        :style="{ color: `grey`, textAlign: `center` }"
                      >
                        <span
                          >Powered by
                          <span
                            :style="{
                              color: `#757575`,
                              fontWeight: `bold`,
                            }"
                            >AWS Cognito</span
                          >
                        </span>
                      </p>
                    </v-card-text>
                  </v-card>
                  <v-divider
                    class="border-opacity-50 my-15"
                    color="grey"
                    vertical
                  />
                  <!-- trial -->
                  <v-card
                    elevation="0"
                    class="pa-4 rounded-xl card-landing-top"
                    :style="{ height: `100%`, width: `50%` }"
                  >
                    <v-card-title>
                      <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                        Trial 🔥
                      </p>
                      <p :style="{ fontSize: `0.8em` }">
                        "Start Your Free Trial Today!"
                      </p>
                      <p :style="{ fontSize: `0.8em` }">
                        &nbsp;Unlock the
                        <span
                          class="gradient-text"
                          :style="{ fontWeight: `bold` }"
                          >Power of AI</span
                        >.
                      </p>
                      <p :style="{ fontSize: `0.8em` }">
                        &nbsp;Discover the new possibilities!
                      </p>
                    </v-card-title>
                    <v-card-text
                      class="pb-0"
                      :style="{
                        height: `calc(100% - 165px)`,
                        overflowX: `auto`,
                        display: `flex`,
                        alignItems: `center`,
                        flexDirection: `column`,
                        justifyContent: `flex-start`,
                      }"
                    >
                      <p
                        class="mb-10 mt-5"
                        :style="{ color: `grey`, textAlign: `center` }"
                      >
                        {{
                          !alreadyGetTrial
                            ? `"Start your free trial here."`
                            : `"We'll contact you shortly."`
                        }}
                      </p>
                      <v-btn
                        :disabled="alreadyGetTrial"
                        class="get-trial-btn rounded-lg"
                        color="primary"
                        @click="trialDialog = true"
                        elevation="10"
                        :style="{ width: `15em` }"
                      >
                        {{
                          !alreadyGetTrial
                            ? `Get Trial for Free`
                            : `Request Submitted!`
                        }}
                      </v-btn>
                      <p
                        class="mt-10"
                        :style="{ color: `grey`, textAlign: `center` }"
                      >
                        <span v-if="!alreadyGetTrial"
                          >"No charge, no commitment <br />
                          just a quick follow-up to get you started."</span
                        >
                        <span v-else
                          >In a hurry? Call us now at
                          <span
                            :style="{
                              color: `#757575`,
                              fontWeight: `bold`,
                            }"
                            >+66 2 640 1151</span
                          >
                          for quick assistance.</span
                        >
                      </p>
                    </v-card-text>
                  </v-card>
                </v-card>
              </v-carousel-item>
              <!-- trial <= 880 -->
              <v-carousel-item v-if="windowWidth <= 880">
                <v-card
                  elevation="0"
                  class="pa-4 rounded-xl card-landing-top"
                  :style="{ height: `100%` }"
                >
                  <v-card-title>
                    <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                      Trial 🔥
                    </p>
                    <p :style="{ fontSize: `0.8em` }">
                      "Start Your Free Trial Today!"
                    </p>
                    <p :style="{ fontSize: `0.8em` }">
                      &nbsp;Unlock the
                      <span
                        class="gradient-text"
                        :style="{ fontWeight: `bold` }"
                        >Power of AI</span
                      >.
                    </p>
                    <p :style="{ fontSize: `0.8em` }">
                      &nbsp;Discover the new possibilities!
                    </p>
                  </v-card-title>
                  <v-card-text
                    class="pb-0"
                    :style="{
                      height: `calc(100% - 165px)`,
                      overflowX: `auto`,
                      display: `flex`,
                      alignItems: `center`,
                      flexDirection: `column`,
                      justifyContent: `flex-start`,
                    }"
                  >
                    <p
                      class="mb-10 mt-5"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      {{
                        !alreadyGetTrial
                          ? `"Start your free trial here."`
                          : `"We'll contact you shortly."`
                      }}
                    </p>
                    <v-btn
                      :disabled="alreadyGetTrial"
                      class="get-trial-btn rounded-lg"
                      color="primary"
                      @click="trialDialog = true"
                      elevation="10"
                      :style="{ width: `15em` }"
                    >
                      {{
                        !alreadyGetTrial
                          ? `Get Trial for Free`
                          : `Request Submitted!`
                      }}
                    </v-btn>
                    <p
                      class="mt-10"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      <span v-if="!alreadyGetTrial"
                        >"No charge, no commitment <br />
                        just a quick follow-up to get you started."</span
                      >
                      <span v-else
                        >In a hurry? Call us now at
                        <span
                          :style="{
                            color: `#757575`,
                            fontWeight: `bold`,
                          }"
                          >+66 2 640 1151</span
                        >
                        for quick assistance.</span
                      >
                    </p>
                  </v-card-text>
                </v-card>
              </v-carousel-item>
              <!-- login <= 880 -->
              <!-- <v-carousel-item v-if="windowWidth <= 880">
                <v-card
                  elevation="0"
                  class="pa-4 rounded-xl card-landing-top"
                  :style="{ height: `100%` }"
                >
                  <v-card-title>
                    <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                      Login 🔑
                    </p>
                    <p :style="{ fontSize: `0.8em` }">"Start Your Journey"</p>
                    <p :style="{ fontSize: `0.8em` }">
                      &nbsp;Smarter, faster, easier service.
                    </p>
                    <p :style="{ fontSize: `0.8em` }">
                      &nbsp;with the
                      <span
                        class="gradient-text"
                        :style="{ fontWeight: `bold` }"
                        >Power of AI</span
                      >.
                    </p>
                  </v-card-title>
                  <v-card-text
                    class="pb-0"
                    :style="{
                      height: `calc(100% - 64px)`,
                      overflowX: `auto`,
                      display: `flex`,
                      alignItems: `center`,
                      flexDirection: `column`,
                      justifyContent: `flex-start`,
                    }"
                  >
                    <p
                      class="mb-10 mt-5"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      Log In to Begin Experience AI Power
                    </p>
                    <v-btn
                      class="get-login-page-btn rounded-lg"
                      color="primary"
                      elevation="10"
                      :style="{ width: `15em` }"
                    >
                      Login
                    </v-btn>

                    <p
                      class="mt-10"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      <span
                        >Powered by
                        <span
                          :style="{
                            color: `#757575`,
                            fontWeight: `bold`,
                          }"
                          >AWS Cognito</span
                        >
                        for unmatched reliability and protection.</span
                      >
                    </p>
                  </v-card-text>
                </v-card>
              </v-carousel-item> -->
            </v-carousel>
          </v-col>
        </v-row>

        <!-- Features Section -->
        <v-row id="features" class="pb-5" :style="{ paddingTop: `60px` }">
          <v-col cols="12">
            <v-card elevation="0">
              <v-card-title class="d-flex justify-center py-6">
                <h2
                  class="text-center font-weight-bold"
                  :style="{ color: `#34495e` }"
                >
                  Feature
                </h2>
              </v-card-title>

              <v-card-text class="text-center px-8">
                <p :style="{ color: `#7f8c8d` }">
                  Discover cutting-edge tools and solutions designed to
                  streamline your workflow, enhance creativity, and drive
                  business success.
                </p>
              </v-card-text>
              <v-card-text>
                <v-container>
                  <v-row
                    :style="{
                      display: `flex`,
                      justifyContent: `center`,
                    }"
                  >
                    <v-col
                      class="pa-10 rounded-xl"
                      :style="{ maxWidth: `805px`, backgroundColor: `#f5f5f5` }"
                    >
                      <div
                        v-for="(category, categoryIndex) in menu"
                        :key="categoryIndex"
                      >
                        <div
                          v-for="(feature, featureIndex) in category"
                          :key="featureIndex"
                          class="mb-2"
                          :disabled="feature.disabled"
                          :style="{
                            display: `flex`,
                            alignItems: `center`,
                            justifyContent:
                              featureIndex % 3 === 0
                                ? `flex-start`
                                : `flex-end`,
                          }"
                        >
                          <v-tooltip location="bottom">
                            <template v-slot:activator="{ props }">
                              <div
                                v-bind="props"
                                :style="{
                                  display: `flex`,
                                  alignItems: `start`,
                                  cursor: `pointer`,
                                  transition: `transform 0.2s ease-in-out`,
                                  filter:
                                    featureHover.trim().length < 1
                                      ? ``
                                      : feature.name === featureHover
                                      ? ``
                                      : `blur(3px)`,
                                  maxWidth: `100%`,
                                }"
                                class="hover-scale"
                                @mouseover="featureHover = feature.name"
                                @mouseleave="featureHover = ``"
                              >
                                <v-chip
                                  v-if="featureIndex % 3 === 0"
                                  :prepend-icon="feature.icon"
                                  class="mr-2 chip_feature_landing_icon"
                                >
                                </v-chip>
                                <v-card
                                  class="py-2 px-4 rounded-xl"
                                  elevation="0"
                                  :style="{
                                    backgroundColor:
                                      featureIndex % 3 === 0
                                        ? `#8eff8e`
                                        : `rgb(219 219 219)`,
                                  }"
                                >
                                  <div>
                                    {{ feature.name }}
                                  </div>
                                </v-card>
                                <v-chip
                                  v-if="featureIndex % 3 !== 0"
                                  :prepend-icon="feature.icon"
                                  class="ml-2 chip_feature_landing_icon"
                                >
                                </v-chip>
                              </div>
                            </template>
                            <div>
                              <p
                                :style="{
                                  fontSize: `0.95rem`,
                                  fontWeight: `bold`,
                                }"
                              >
                                {{ feature.name }}
                              </p>
                              <span
                                class="break-word"
                                :style="{
                                  fontSize: `0.8rem`,
                                }"
                                >{{ feature.description }}</span
                              >
                            </div>
                          </v-tooltip>
                        </div>
                      </div>
                      <div
                        class="mt-10"
                        :style="{
                          filter:
                            featureHover.trim().length >= 1 ? `blur(3px)` : ``,
                        }"
                      >
                        <v-text-field
                          :disabled="alreadyGetTrial"
                          v-model="featureText"
                          hide-details
                          density="compact"
                          variant="outlined"
                          :append-inner-icon="`mdi-send-variant`"
                          :placeholder="`Write something...`"
                          @keyup.enter="clickInteresting()"
                          @click:appendInner="clickInteresting()"
                        ></v-text-field>
                      </div>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Trusted Customers Section -->
        <v-row
          id="trustedCustomers"
          class="pb-5"
          :style="{ paddingTop: `60px`, backgroundColor: `#f5f6fa` }"
        >
          <v-col cols="12">
            <v-card
              class="elevation-0"
              :style="{
                display: `flex`,
                flexDirection: `column`,
                alignItems: `center`,
                backgroundColor: `#f5f6fa`,
              }"
            >
              <v-card-title class="d-flex justify-center py-6">
                <h2
                  class="text-center font-weight-bold"
                  :style="{ color: `#34495e` }"
                >
                  Our Trusted Customers
                </h2>
              </v-card-title>

              <v-card-text class="text-center px-8">
                <p :style="{ color: `#7f8c8d` }">
                  Join a growing list of satisfied customers who trust us for
                  our exceptional services.
                </p>
              </v-card-text>
              <v-card-text :style="{ maxWidth: `800px`, width: `100%` }">
                <v-container>
                  <v-row>
                    <v-col
                      cols="3"
                      class="pa-4"
                      v-for="(item, idx) in customers"
                      :key="`landing_trusted_customer_${idx}`"
                    >
                      <v-tooltip location="bottom">
                        <template v-slot:activator="{ props }">
                          <v-avatar
                            class="hover-scale"
                            v-bind="props"
                            :style="{
                              height: `100%`,
                              width: `100%`,
                              maxHeight: `150px`,
                              maxWidth: `150px`,
                              aspectRatio: `1`,
                              cursor: `pointer`,
                            }"
                          >
                            <v-img :src="item.img"></v-img>
                          </v-avatar>
                        </template>
                        <span>{{ item.name }}</span>
                      </v-tooltip>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Pricing Section -->
        <v-row id="pricing" class="pb-5" :style="{ paddingTop: `100px` }">
          <v-col cols="12">
            <v-card elevation="0" class="rounded-lg">
              <v-card-title class="d-flex justify-center">
                <h2
                  class="text-center font-weight-bold"
                  :style="{ color: `#34495e` }"
                >
                  Flexible Pricing Plans
                </h2>
              </v-card-title>

              <v-card-text class="text-center">
                <p :style="{ color: `#7f8c8d`, fontSize: `1rem` }">
                  Choose the plan that fits your needs. Our pricing is
                  transparent and flexible based on the features you require.
                </p>
              </v-card-text>

              <v-card-text>
                <v-container>
                  <!-- Plan Selector -->
                  <v-row class="justify-center">
                    <!-- Starter Plan (Green - Common) -->
                    <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        @click="compareDialog = true"
                        class="pa-4 rounded-lg hover-tilt-glow"
                        :style="{
                          background:
                            'linear-gradient(90deg, rgba(210, 245, 210, 1) 0%, rgba(180, 235, 200, 1) 100%)',
                          height: `100%`,
                          cursor: `pointer`,
                        }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#3a6b47` }"
                          >
                            Starter Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#588564` }"
                        >
                          A great plan to get started.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#a8d3a8` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#4caf50` }"
                          >
                            From $19/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#588564` }">
                            Basic tools for individuals and small teams.
                          </p>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Professional Plan (Blue - Rare) -->
                    <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        @click="compareDialog = true"
                        class="pa-4 rounded-lg hover-tilt-glow"
                        :style="{
                          background:
                            'linear-gradient(90deg, rgba(210, 235, 255, 1) 0%, rgba(180, 220, 250, 1) 100%)',
                          height: `100%`,
                          cursor: `pointer`,
                        }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#3a5780` }"
                          >
                            Professional Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#526b8f` }"
                        >
                          Ideal for growing teams.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#b5d4f5` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#2979ff` }"
                          >
                            From $49/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#526b8f` }">
                            Advanced features for collaboration and
                            productivity.
                          </p>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Enterprise Plan (Yellow - Legendary) -->
                    <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        @click="compareDialog = true"
                        class="pa-4 rounded-lg hover-tilt-glow"
                        :style="{
                          background:
                            'linear-gradient(90deg, rgba(255, 244, 200, 1) 0%, rgba(255, 229, 150, 1) 100%)',
                          height: `100%`,
                          cursor: `pointer`,
                        }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#b7860c` }"
                          >
                            Enterprise Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#8f6f0a` }"
                        >
                          The ultimate plan for large organizations.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#ffdd80` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#ffa000` }"
                          >
                            Contact us for pricing
                          </h4>
                          <p class="mt-2" :style="{ color: `#8f6f0a` }">
                            Premium tools and dedicated support for enterprises.
                          </p>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Basic Plan -->
                    <!-- <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        @click="compareDialog = true"
                        class="pa-4 rounded-lg hover-tilt-glow"
                        :style="{
                          backgroundColor: `#dbe9f1`,
                          height: `100%`,
                          cursor: `pointer`,
                        }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#34495e` }"
                          >
                            Standard Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#7f8c8d` }"
                        >
                          Plan for individuals.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#b2bec3` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#2980b9` }"
                          >
                            From $19/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#7f8c8d` }">
                            Basic features for small teams.
                          </p>
                        </div>
                      </v-card>
                    </v-col> -->

                    <!-- Professional Plan -->
                    <!-- <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        @click="compareDialog = true"
                        class="pa-4 rounded-lg hover-tilt-glow"
                        :style="{
                          backgroundColor: `#ffeaa7`,
                          height: `100%`,
                          cursor: `pointer`,
                        }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#b7950b` }"
                          >
                            Professional Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#7f8c8d` }"
                        >
                          Perfect for professionals.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#d4ac0d` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#b7950b` }"
                          >
                            From $49/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#7f8c8d` }">
                            Enhanced features for professional teams.
                          </p>
                        </div>
                      </v-card>
                    </v-col> -->

                    <!-- Enterprise Plan -->
                    <!-- <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        @click="compareDialog = true"
                        class="pa-4 rounded-lg hover-tilt-glow"
                        :style="{
                          background:
                            'linear-gradient(90deg, rgba(242, 195, 235, 1) 9%, rgba(217, 212, 252, 1) 77%)',
                          height: `100%`,
                          cursor: `pointer`,
                        }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#8e44ad` }"
                          >
                            Enterprise Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#2f3640` }"
                        >
                          Plan for enterprise
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#e0a9c7` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#8e44ad` }"
                          >
                            From $0/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#7f8c8d` }">
                            All Features and premium support.
                          </p>
                        </div>
                      </v-card>
                    </v-col> -->
                  </v-row>
                  <v-row>
                    <v-col
                      cols="12"
                      :style="{
                        display: `flex`,
                        justifyContent: `center`,
                        flexDirection: `column`,
                        alignItems: `center`,
                      }"
                    >
                      <v-btn
                        :style="{
                          backgroundColor: `#f3f3f3`,
                        }"
                        variant="outlined"
                        rounded
                        class="compare-btn"
                        @click="compareDialog = true"
                      >
                        Compare Plans
                        <v-icon>mdi-chevron-double-down</v-icon>
                      </v-btn>
                      <!-- <span
                        class="mt-3"
                        :style="{ fontSize: `0.7rem`, color: `grey` }"
                        >* "If you choose the custom plan, you can tailor the
                        features to suit your needs, based on your specific
                        requirements."</span
                      > -->
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Technologies We Trust Section -->
        <v-row
          id="technologiesWeTrust"
          class="pb-5"
          :style="{ paddingTop: `60px`, backgroundColor: `rgb(208, 223, 249)` }"
        >
          <v-col cols="12">
            <v-card
              class="elevation-0"
              :style="{
                display: `flex`,
                flexDirection: `column`,
                alignItems: `center`,
                backgroundColor: `rgb(208, 223, 249)`,
              }"
            >
              <v-card-title class="d-flex justify-center py-6">
                <h2
                  class="text-center font-weight-bold"
                  :style="{ color: `#34495e` }"
                >
                  Technologies We Trust
                </h2>
              </v-card-title>

              <v-card-text class="text-center px-8">
                <p :style="{ color: `#7f8c8d` }">
                  We utilize cutting-edge technologies to deliver the best
                  performance and security for our users.
                </p>
              </v-card-text>

              <v-card-text :style="{ maxWidth: `1000px`, width: `100%` }">
                <v-container>
                  <v-row>
                    <v-col
                      cols="4"
                      class="pa-4"
                      v-for="(tech, idx) in technologies"
                      :key="`landing_technology_${idx}`"
                      :style="{
                        display: `flex`,
                        justifyContent: `center`,
                      }"
                    >
                      <v-tooltip location="bottom">
                        <template v-slot:activator="{ props }">
                          <v-avatar
                            class="hover-bounce"
                            v-bind="props"
                            :style="{
                              height: `100%`,
                              width: `100%`,
                              maxHeight: `100px`,
                              maxWidth: `100px`,
                              aspectRatio: `1`,
                              cursor: `pointer`,
                            }"
                          >
                            <v-img :src="tech.img" alt="tech.name"></v-img>
                          </v-avatar>
                        </template>
                        <div>
                          <p
                            :style="{
                              fontSize: `0.95rem`,
                              fontWeight: `bold`,
                            }"
                          >
                            {{ tech.name }}
                          </p>
                          <span
                            class="break-word"
                            :style="{
                              fontSize: `0.8rem`,
                            }"
                            >{{ tech.description }}</span
                          >
                        </div>
                      </v-tooltip>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <!-- Footer Section -->
    <v-footer
      app
      :style="{
        backgroundColor: `rgba(244, 244, 249, ${
          scrollPosition - 60 >= 1 ? `1` : `0`
        })`,
      }"
    >
      <v-col class="text-center">
        <p>
          &copy; 2024 4Plus Consulting Co. Ltd
          <span v-if="windowWidth > 615">
            | Contact us:
            <span :style="{ fontWeight: `bold` }">+66 2 640 1151</span>
            (Thailand)
          </span>
        </p>
      </v-col>
    </v-footer>

    <!-- trial dialog -->
    <v-dialog v-model="trialDialog" max-width="600px">
      <v-card class="pa-6 rounded-xl">
        <v-card-title class="headline"
          >Request Your Free Trial 🔑
        </v-card-title>
        <v-card-text class="pb-0">
          <v-form>
            <v-text-field
              hint="*Required"
              persistent-hint
              class="mb-3"
              rounded="xl"
              variant="outlined"
              label="Name"
              :rules="[(v) => !!v || 'Name is required']"
              v-model="form.name"
              required
            ></v-text-field>
            <v-text-field
              hint="*Required"
              persistent-hint
              class="mb-3"
              rounded="xl"
              variant="outlined"
              label="Email"
              :rules="[
                (v) => !!v || 'Email is required',
                (v) => /.+@.+\..+/.test(v) || 'Email must be valid',
              ]"
              v-model="form.email"
              required
              type="email"
            ></v-text-field>
            <v-text-field
              hint="*Required"
              persistent-hint
              class="mb-3"
              rounded="xl"
              variant="outlined"
              label="Company Name"
              :rules="[(v) => !!v || 'Company Name is required']"
              v-model="form.company"
              required
            ></v-text-field>
            <v-textarea
              class="mb-3"
              rounded="xl"
              variant="outlined"
              label="Message"
              v-model="form.message"
              required
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="trialDialog = false">Cancel</v-btn>
          <v-btn
            :disabled="validateForm()"
            @click="clickSubmitRequestTrial()"
            :style="{
              backgroundColor: `#00c853`,
              color: `white`,
              minWidth: `100px`,
            }"
            >Submit</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- interesting dialog -->
    <v-dialog v-model="interestingDialog" max-width="600px">
      <v-card class="pa-6 rounded-xl shake">
        <v-card-title
          class="headline"
          :style="{
            display: `flex`,
            justifyContent: `space-between`,
            alignItems: `center`,
          }"
        >
          <span
            ><span :style="{ fontWeight: `bold`, fontSize: `1.5rem` }"
              >Interested?
            </span></span
          >
          <v-btn
            icon="mdi-close"
            variant="fab"
            @click="interestingDialog = false"
          ></v-btn>
        </v-card-title>
        <v-card-text class="pb-0 pt-1">
          <p>
            "It looks like you're interested in our app! You can request a free
            trial right now."
          </p>
        </v-card-text>
        <v-card-actions>
          <!-- <v-btn text @click="interestingDialog = false">Cancel</v-btn> -->
          <div
            class="pa-10"
            :style="{ display: `flex`, justifyContent: `center` }"
          >
            <v-btn
              @click="clickInterestingRequest()"
              class="get-trial-btn"
              :style="{
                backgroundColor: `#00c853`,
                color: `white`,
                minWidth: `100px`,
              }"
              >Request Trial</v-btn
            >
          </div>
        </v-card-actions>
        <v-card-text class="pt-0">
          <p :style="{ fontSize: `0.75rem`, color: `grey` }">
            "If you need immediate assistance, feel free to contact us at
            <span :style="{ fontWeight: `bold` }">+66 2 640 1151</span>
          </p>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- compare dialog -->
    <v-dialog
      v-model="compareDialog"
      max-width="850px"
      transition="dialog-bottom-transition"
    >
      <v-card class="pa-6 rounded-xl">
        <v-card-title
          class="headline"
          :style="{
            display: `flex`,
            justifyContent: `space-between`,
            alignItems: `center`,
          }"
        >
          Compare 🔍
          <v-btn
            icon="mdi-close"
            variant="fab"
            @click="compareDialog = false"
          ></v-btn>
        </v-card-title>
        <v-card-text class="pb-0 pt-0 px-1 rounded-lg">
          <v-table>
            <thead>
              <tr>
                <th class="text-center table-feature-head">Feature</th>
                <th class="text-center table-standard-head">Standard</th>
                <th class="text-center table-professional-head">
                  Professional
                </th>
                <th class="text-center table-enterprise-head">Enterprise</th>
                <!-- <th class="text-left">Custom</th> -->
              </tr>
            </thead>
            <tbody>
              <tr
                class="tableBody"
                v-for="item in itemTable"
                :key="`table_pricing_${item.name}`"
              >
                <td class="px-0">
                  <v-icon>{{ item.icon }}</v-icon
                  >&nbsp;
                  {{ item.name }}
                </td>
                <td
                  class="table-standard"
                  :style="{
                    textAlign: `center`,
                  }"
                >
                  {{ item.standard }}
                  <p
                    v-if="
                      item.name === 'Integration API' || item.name === 'Channel'
                    "
                  >
                    {{ item.BRstandard }}
                  </p>
                </td>
                <td
                  class="table-professional"
                  :style="{
                    textAlign: `center`,
                  }"
                >
                  {{ item.profressional }}
                  <p
                    v-if="
                      item.name === 'Integration API' || item.name === 'Channel'
                    "
                  >
                    {{ item.BRprofressional }}
                  </p>
                </td>
                <td
                  class="table-enterprise"
                  :style="{
                    textAlign: `center`,
                  }"
                >
                  {{ item.enterprise }}
                  <p
                    v-if="
                      item.name === 'Integration API' || item.name === 'Channel'
                    "
                  >
                    {{ item.BRenterprise }}
                  </p>
                </td>
                <!-- <td :style="{ textAlign: `center` }">{{ item.custom }}</td> -->
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!--snackbar-->
    <v-snackbar
      v-model="snackbarAlert"
      timeout="5000"
      :color="snackbarSuccess ? '#5EB491' : '#D6584D'"
      location="top"
      location-strategy="connected"
    >
      <span>
        <v-icon v-if="snackbarSuccess"
          >mdi-checkbox-marked-circle-outline</v-icon
        >
        <v-icon v-else>mdi-alert-circle</v-icon>
        {{ snackbarMsg }}
      </span>

      <template v-slot:action="{ attrs }">
        <v-btn color="white" text v-bind="attrs" @click="snackbarAlert = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      featureText: ``,
      trialDialog: false,
      form: {
        name: "",
        email: "",
        company: "",
        message: "",
      },
      showChat: [
        { type: `customer`, msg: `Hi, I need some help.` },
        { type: `admin`, msg: `Sorry, I’m swamped. Can you wait a bit?` },
        { type: `ai`, msg: `I got this! What’s your issue? 😊` },
        { type: `customer`, msg: `Oh, cool! How do I use this product?` },
        {
          type: `ai`,
          msg: `Easy! Here’s the guide: [link].`,
        },
      ],
      windowWidth: 0,
      windowHeight: 0,
      scrollPosition: 0,
      itemTable: [
        {
          icon: "mdi-message-processing-outline",
          name: "Interaction",
          standard: `60,000(5,000)`,
          profressional: `120,000(10,000)`,
          enterprise: `240,000(20,000)`,
        },
        {
          icon: "mdi-account-key-outline",
          name: "Admin",
          standard: "1",
          profressional: "2",
          enterprise: "3",
        },
        {
          icon: "mdi-account-multiple-outline",
          name: "Agent",
          standard: "1",
          profressional: "2",
          enterprise: "3",
        },
        {
          icon: "mdi-chart-box-outline",
          name: "Report",
          standard: "✅",
          profressional: "✅",
          enterprise: "✅",
        },
        {
          icon: "mdi-emoticon-outline",
          name: "Sentiment Analysis",
          standard: "❌",
          profressional: "✅",
          enterprise: "✅",
        },
        {
          icon: "mdi-lightbulb-outline",
          name: "Summary Ai",
          standard: "❌",
          profressional: "✅",
          enterprise: "✅",
        },
        {
          icon: "mdi-chart-timeline-variant",
          name: "Customer 360 Reports",
          standard: "❌",
          profressional: "❌",
          enterprise: "✅",
        },
        {
          icon: "mdi-message-text-outline",
          name: "Channel",
          standard: "1 Social",
          profressional: "2 Socials",
          enterprise: "3 Socials",
          BRstandard: "Live Chat (Line)",
          BRprofressional: "Live Chat",
          BRenterprise: "Live Chat",
        },
        {
          icon: "mdi-api",
          name: "Integration API",
          standard: "0",
          profressional: "1",
          enterprise: "2-3",
          BRstandard: "200,000(16,666)",
          BRprofressional: "250,000(20,833)",
          BRenterprise: "350,000(29,166)",
        },

        {
          icon: "mdi-cash-multiple",
          name: "One Time Set up Fee",
          standard: "50,000",
          profressional: "50,000",
          enterprise: "50,000",
        },
        {
          icon: "mdi-wrench-outline",
          name: "Implementation",
          standard: "-",
          profressional: "Based on complexity",
          enterprise: "Based on complexity",
        },
      ],
      menu: {
        Communication: [
          {
            icon: "mdi-chat-outline",
            name: "Unified Online Channel Chat",
            description:
              "Streamline customer communication by effortlessly connecting across multiple online channels, creating a unified hub for all your interactions",
          },
        ],
        Data_Insight: [
          {
            icon: "mdi-database",
            name: "Data Warehouse Explorer",
            description:
              "Unlock the potential of your enterprise's data by exploring vast datasets, revealing hidden insights to drive smarter business decisions.",
          },
          {
            icon: "mdi-robot",
            name: "Product Knowledge Hub",
            description:
              "Access a wealth of expert-level product knowledge instantly through an AI-driven chatbot, providing your team with valuable insights for every query.",
          },
        ],
        Design_Partner: [
          {
            icon: "mdi-facebook",
            name: "Facebook Ads with AI",
            description:
              "Harness the power of AI to create highly engaging, data-driven Facebook ad campaigns that resonate with your audience and drive measurable results.",
          },
          {
            icon: "mdi-google",
            name: "Google Ads with AI",
            description:
              "Optimize your Google Ads strategy by leveraging AI to generate compelling ad content, target the right audience, and maximize your ROI.",
          },
          {
            icon: "mdi-lightbulb",
            name: "AI-Powered Product Design",
            description:
              "Collaborate with AI to push the boundaries of creativity and innovation, helping you design your next groundbreaking product with ease.",
          },
        ],
        Support_Function: [
          {
            icon: "mdi-account-group",
            name: "Human Resource",
            description:
              "Streamline HR processes by quickly accessing relevant dashboards to handle employee inquiries and manage HR needs efficiently.",
          },
        ],
        Dashboard_Solutions: [
          {
            icon: "mdi-view-dashboard",
            name: "Smart Dashboard Finder",
            description:
              "Easily discover and access the dashboards that matter most to your team, enabling you to focus on key metrics and decisions without wasting time.",
          },
          {
            icon: "mdi-chart-areaspline",
            name: "AI-Enhanced Automated Dashboards",
            description:
              "Leverage the power of Copilot to automatically create dynamic Power BI dashboards that update in real-time, ensuring you have the latest insights at your fingertips.",
          },
        ],
      },
      core: [
        {
          head: ` Intelligent Chat Analysis`,
          body: `Understand customer questions and needs with precision.`,
          emoji: `💡`,
        },
        {
          head: ` Instant Responses`,
          body: `24/7 automated replies to keep your customers engaged.`,
          emoji: `⚡`,
        },
        {
          head: `Unified Chat Management`,
          body: `Centralize all chats from LINE OA, Facebook, and other platforms in one dashboard.`,
          emoji: `📋`,
        },
        {
          head: `Complete Control`,
          body: `Users can step in anytime to respond and manage conversations.`,
          emoji: `🎛️`,
        },
        {
          head: `Professional Problem Solving`,
          body: `Ensure customer satisfaction with quick and effective issue resolution.`,
          emoji: `🛠️`,
        },
        {
          head: `Insightful Analytics Dashboard`,
          body: `Access a dashboard that analyzes customer needs and tracks responder (admin) performance to enhance service efficiency.`,
          emoji: `📊`,
        },
      ],
      customers: [
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
      ],
      technologies: [
        {
          name: "AWS Web Services (AWS)",
          img: "https://seekvectors.com/files/download/7bc0d5d3fcd01b0bf60c363e4537dc5d.jpg",
          description:
            "AWS provides secure, scalable, and reliable cloud infrastructure to support your business operations with the flexibility and power to scale as your needs grow.",
        },
        {
          name: "OpenAI (ChatGPT)",
          img: "https://openai.com/favicon.ico",
          description:
            "OpenAI’s ChatGPT enables AI-powered conversational capabilities, providing intelligent, human-like interactions and insights to enhance customer service and decision-making.",
        },
        {
          name: "Tableau",
          img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9RQ7-cqafLIVFwKrME-J2qMLNX3J70oLDww&s",
          description:
            "Tableau is a powerful data visualization tool that helps you turn your data into actionable insights through interactive dashboards and reports.",
        },
      ],
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: "untitled",
      alreadyGetTrial: false,
      featureHover: ``,
      interestingDialog: false,
      compareDialog: false,
    };
  },
  mounted() {
    window.addEventListener("scroll", this.trackScroll);
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.trackScroll);
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    // resposive
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    trackScroll() {
      this.scrollPosition = window.scrollY;
    },
    scrollTo(id) {
      const element = document.getElementById(id);
      if (element) {
        element.scrollIntoView({ behavior: "smooth" });
      }
    },
    validateForm() {
      if (!this.form.name || this.form.name.trim() === "") {
        return true;
      }

      const emailPattern = /.+@.+\..+/;
      if (!this.form.email || this.form.email.trim() === "") {
        return true;
      } else if (!emailPattern.test(this.form.email)) {
        return true;
      }

      if (!this.form.company || this.form.company.trim() === "") {
        return true;
      }

      return false;
    },
    //click
    clickInteresting() {
      this.featureText = ``;
      this.interestingDialog = true;
    },
    clickInterestingRequest() {
      this.interestingDialog = false;
      this.trialDialog = true;
    },
    clickSubmitRequestTrial() {
      this.form.name = ``;
      this.form.company = ``;
      this.form.email = ``;
      this.form.message = ``;

      this.trialDialog = false;
      this.alreadyGetTrial = true;
      this.snackbarMsg = `Success! We'll contact you as soon as possible.`;
      this.snackbarSuccess = true;
      this.snackbarAlert = true;
    },
  },
};
</script>

<style scoped>
.card-title-contact-dialog {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.card-landing-top {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.div-app-bar {
  font-weight: bold;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
.landing-page {
  background: rgb(242, 195, 235);
  background: linear-gradient(
    180deg,
    rgba(242, 195, 235, 1) 9%,
    rgba(217, 212, 252, 1) 77%
  );
  background: linear-gradient(
    270deg,
    rgba(242, 195, 235, 1) 10%,
    rgba(229, 216, 245, 1) 40%,
    rgba(217, 212, 252, 1) 70%,
    rgba(201, 234, 247, 1) 100%
  );

  background-size: 400% 400%;
  animation: bgAnimation 12s ease infinite;
}

.landing-layout {
  width: 100%;
  position: fixed;
  display: flex;
  flex-direction: row;
  align-items: center;
  z-index: 99;
  background: linear-gradient(
    270deg,
    rgba(242, 195, 235, 1) 10%,
    rgba(229, 216, 245, 1) 40%,
    rgba(242, 195, 235, 1) 50%,
    rgba(217, 212, 252, 1) 70%,
    rgba(201, 234, 247, 1) 100%
  );

  background-size: 400% 400%;
  animation: bgAnimation 12s ease infinite;
}

.v-footer {
  background-color: #f4f4f9;
}

.hidden {
  display: none;
}
.get-trial-btn {
  background: linear-gradient(45deg, #c87100, #a9ac16);
  color: white;
  font-weight: bold;
  font-size: 18px;
  border-radius: 50px;
  padding: 12px 40px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 35%;
}

.get-trial-btn:hover {
  background: linear-gradient(45deg, #ffa42c, #d5d80b);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.get-trial-btn:active {
  transform: scale(0.98);
}

.get-trial-btn:focus {
  outline: none;
}

.get-login-btn {
  display: flex;
  background: linear-gradient(45deg, #00c853, #00bfae);
  color: white;
  font-weight: bold;
  font-size: 18px;
  border-radius: 50px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
}

.get-login-btn:hover {
  background: linear-gradient(45deg, #00bfae, #00c853);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.get-login-btn:active {
  transform: scale(0.98);
}

.get-login-btn:focus {
  outline: none;
}

.get-login-page-btn {
  background: linear-gradient(45deg, #00c853, #00bfae);
  color: white;
  font-weight: bold;
  font-size: 18px;
  border-radius: 50px;
  padding: 12px 40px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 35%;
}

.get-login-page-btn:hover {
  background: linear-gradient(45deg, #00bfae, #00c853);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.get-login-page-btn:active {
  transform: scale(0.98);
}

.get-login-page-btn:focus {
  outline: none;
}
.chip_feature_landing_icon {
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
}

.hover-scale:hover {
  transform: scale(1.2);
  z-index: 999;
}

span.break-word {
  display: inline-block;
  max-width: 300px;
  word-wrap: break-word;
}

span.break-word-chip {
  display: inline-block;
  max-width: 100%;
  word-wrap: break-word;
}

.compare-btn {
  text-transform: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.compare-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.ellipsis-text {
  display: inline-block;
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/*table*/

.table-standard {
  background: linear-gradient(
    90deg,
    rgb(210, 245, 210) 0%,
    rgb(180, 235, 200) 100%
  );
  font-weight: bold;
  font-size: 0.8rem;
  color: rgb(58, 107, 71);
}
.table-professional {
  background: linear-gradient(
    90deg,
    rgb(210, 235, 255) 0%,
    rgb(180, 220, 250) 100%
  );
  font-weight: bold;
  font-size: 0.8rem;
  color: rgb(58, 87, 128);
}
.table-enterprise {
  background: linear-gradient(
    90deg,
    rgb(255, 244, 200) 0%,
    rgb(255, 229, 150) 100%
  );
  font-weight: bold;
  font-size: 0.8rem;
  color: rgb(183, 134, 12);
}

.table-feature-head {
  width: 270px;
}
.table-standard-head {
  background: linear-gradient(
    90deg,
    rgb(210, 245, 210) 0%,
    rgb(180, 235, 200) 100%
  );

  color: rgb(76, 175, 80);
  font-weight: bold;
  font-size: 1rem;
  width: 200px;
}
.table-professional-head {
  background: linear-gradient(
    90deg,
    rgb(210, 235, 255) 0%,
    rgb(180, 220, 250) 100%
  );
  color: rgb(41, 121, 255);
  font-weight: bold;
  font-size: 1rem;
  width: 200px;
}
.table-enterprise-head {
  background: linear-gradient(
    90deg,
    rgb(255, 244, 200) 0%,
    rgb(255, 229, 150) 100%
  );
  color: rgb(255, 160, 0);
  font-weight: bold;
  font-size: 1rem;
  width: 200px;
}

.tableBody:hover {
  transform: scale(0.9);
  cursor: pointer;
  border: solid 1px black !important;
}
</style>
