<template>
  <v-card class="rounded-xl" :style="{ height: `calc(100dvh - 110px)` }">
    <v-card-title>
      <p
        class="gradient-text"
        :style="{
          fontWeight: 'bold',
          whiteSpace: `nowrap`,
          overflow: `hidden`,
          textOverflow: `ellipsis`,
        }"
      >
        {{
          botMode === `edit`
            ? `Customize Your Chatbot Settings`
            : `Build Your Personalized Chatbot!`
        }}
      </p>
      <span :style="{ fontSize: '0.8rem', color: 'grey' }">
        {{
          botMode === `edit`
            ? `${item.name}: Adjust settings.`
            : `Set up your chatbot.`
        }}
      </span>
    </v-card-title>

    <v-card-text
      class="py-0 px-1"
      :style="{
        overflowY: `hidden`,
        overflowX: `hidden`,
        height: `calc(100% - 80px)`,
        width: `100%`,
        overflowY: `auto`,
      }"
    >
      <v-container
        :style="{ height: `100%`, display: `flex`, alignItems: `center` }"
      >
        <v-row :style="{ height: `100%`, width: `100%` }">
          <v-col
            :cols="windowWidth > 1100 ? 6 : 12"
            :style="{ height: `calc(100%)`, width: `100%` }"
          >
            <v-card
              elevation="0"
              class="rounded-xl"
              :style="{ height: `100%`, border: `solid 1px lightgrey` }"
            >
              <v-card-text class="px-1 pb-4 pt-3">
                <v-row>
                  <v-col
                    v-for="(item, idx) in menuItems"
                    @click="
                      selectedMenu = { id: item.id, menuKey: item.menuKey }
                    "
                    :key="`menu_digitalTwin_${idx}`"
                    cols="4"
                    :style="{
                      border:
                        idx !== selectedMenu.id ? `solid 1px lightgrey` : ``,
                      borderTop: `none`,
                      borderBottomLeftRadius:
                        idx === selectedMenu.id + 1 ? `25px` : ``,
                      borderBottomRightRadius:
                        idx === selectedMenu.id - 1 ? `25px` : ``,
                      borderBottom:
                        selectedMenu.id === item.id
                          ? ``
                          : `solid 1px lightgrey`,
                      backgroundColor: item.disabled
                        ? `lightgrey`
                        : selectedMenu.id === item.id
                        ? ``
                        : `#efefef`,
                      cursor: item.disabled ? `` : `pointer`,
                      pointerEvents: item.disabled ? `none` : ``,
                      filter: item.disabled ? `grayscale(1)` : ``,
                      fontWeight: item.id === selectedMenu.id ? `bold` : ``,
                    }"
                  >
                    <div>
                      <p>{{ item.icon }}</p>
                      <p
                        :style="{
                          whiteSpace: `nowrap`,
                          overflow: `hidden`,
                          textOverflow: `ellipsis`,
                        }"
                      >
                        {{ item.name }}
                      </p>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
              <v-card-text
                v-if="selectedMenu.menuKey === `defineChatbot`"
                :style="{
                  height:
                    windowWidth <= 500
                      ? `calc(100% - 220px)`
                      : `calc(100% - 135px)`,
                  overflowY: `auto`,
                }"
              >
                <v-form ref="form">
                  <div
                    v-for="(key, idx) in Object.keys(
                      setupItem[selectedMenu.menuKey]
                    )"
                    :key="`${
                      setupItem[selectedMenu.menuKey][key].id
                    }_form${key}`"
                    class="pt-4 px-4"
                  >
                    <div class="mb-2">
                      <p :style="{ textAlign: `center` }">
                        {{ setupItem[selectedMenu.menuKey][key].description }}
                      </p>
                    </div>
                    <!-- Text input field -->
                    <div
                      v-if="
                        setupItem[selectedMenu.menuKey][key].type === 'text'
                      "
                    >
                      <div
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                        }"
                      >
                        <v-text-field
                          :label="menuNamed(key)"
                          density="compact"
                          variant="outlined"
                          :style="{ borderRadius: '8px', maxWidth: `500px` }"
                          v-model="setupItem[selectedMenu.menuKey][key].value"
                          :rules="[
                            requiredRule(setupItem[selectedMenu.menuKey][key]),
                          ]"
                        />
                      </div>
                    </div>
                    <!-- Textarea input field -->
                    <div
                      v-else-if="
                        setupItem[selectedMenu.menuKey][key].type === 'textarea'
                      "
                    >
                      <div
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                        }"
                      >
                        <v-textarea
                          :label="menuNamed(key)"
                          density="compact"
                          variant="outlined"
                          :style="{ borderRadius: '8px', maxWidth: `500px` }"
                          v-model="setupItem[selectedMenu.menuKey][key].value"
                          :rules="[
                            requiredRule(setupItem[selectedMenu.menuKey][key]),
                          ]"
                        />
                      </div>
                    </div>
                    <!-- Autocomplete field -->
                    <div
                      v-else-if="
                        setupItem[selectedMenu.menuKey][key].type ===
                        'autocomplete'
                      "
                    >
                      <div
                        v-if="
                          setupItem[selectedMenu.menuKey][key].key ===
                          `line_integration_uuid`
                        "
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                        }"
                      >
                        <v-autocomplete
                          v-model="setupItem[selectedMenu.menuKey][key].value"
                          :items="setupItem[selectedMenu.menuKey][key].item"
                          :label="menuNamed(key)"
                          :item-value="`uuid`"
                          :item-title="`username`"
                          variant="outlined"
                          density="compact"
                          :style="{ borderRadius: '8px', maxWidth: `500px` }"
                          :rules="[
                            requiredRule(setupItem[selectedMenu.menuKey][key]),
                          ]"
                        />
                      </div>
                      <div
                        v-else
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                        }"
                      >
                        <v-autocomplete
                          v-model="setupItem[selectedMenu.menuKey][key].value"
                          :items="setupItem[selectedMenu.menuKey][key].item"
                          :label="menuNamed(key)"
                          variant="outlined"
                          density="compact"
                          :style="{ borderRadius: '8px', maxWidth: `500px` }"
                          :rules="[
                            requiredRule(setupItem[selectedMenu.menuKey][key]),
                          ]"
                        />
                      </div>
                    </div>
                    <!-- Autocomplete Multiple field -->
                    <div
                      v-else-if="
                        setupItem[selectedMenu.menuKey][key].type ===
                        'autocomplete-multiple'
                      "
                    >
                      <div
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                        }"
                      >
                        <v-autocomplete
                          v-model="setupItem[selectedMenu.menuKey][key].value"
                          :items="setupItem[selectedMenu.menuKey][key].item"
                          :label="menuNamed(key)"
                          multiple
                          variant="outlined"
                          density="compact"
                          :style="{ borderRadius: '8px', maxWidth: `500px` }"
                          :rules="[
                            requiredRule(setupItem[selectedMenu.menuKey][key]),
                          ]"
                        />
                      </div>
                    </div>
                    <!-- Boolean (Checkbox) field -->
                    <div
                      v-if="
                        setupItem[selectedMenu.menuKey][key].type === 'boolean'
                      "
                    >
                      <div
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                        }"
                      >
                        <v-switch
                          v-model="setupItem[selectedMenu.menuKey][key].value"
                          :label="
                            setupItem[selectedMenu.menuKey][key].value
                              ? `Yes`
                              : `No`
                          "
                          inset
                          :color="`#15d766`"
                        />
                      </div>
                    </div>
                    <v-divider
                      class="my-2"
                      v-if="idx < setupItem[selectedMenu.menuKey].length - 1"
                      :style="{ maxWidth: '500px', margin: 'auto' }"
                    />
                  </div>
                </v-form>
              </v-card-text>
              <v-card-text
                v-else-if="selectedMenu.menuKey !== `defineChatbot`"
                :style="{
                  height:
                    windowWidth <= 500
                      ? `calc(100% - 220px)`
                      : `calc(100% - 135px)`,
                  overflowY: `auto`,
                }"
              >
                <v-row>
                  <v-col
                    :cols="windowWidth >= 1300 ? 4 : windowWidth < 420 ? 12 : 6"
                  >
                    <v-card
                      @click="clickOpenDialog(null, 0, selectedMenu.menuKey)"
                      class="rounded-xl hover-card"
                      :style="{
                        border: `solid 1px lightgrey`,
                        minHeight: `144.73px`,
                        display: `flex`,
                        alignItems: `center`,
                        justifyContent: `center`,
                      }"
                    >
                      <div
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                          alignItems: `center`,
                          height: `100%`,
                          flexDirection: `column`,
                        }"
                      >
                        <div>
                          <span
                            :style="{ fontWeight: `bold`, fontSize: `1rem` }"
                            >Add More
                          </span>
                        </div>
                        <div>
                          <v-icon
                            :style="{
                              color: '#5EB491',
                              fontSize: `2.5rem`,
                            }"
                          >
                            mdi-plus-circle
                          </v-icon>
                        </div>
                      </div>
                    </v-card>
                  </v-col>
                  <v-col
                    :cols="windowWidth >= 1300 ? 4 : windowWidth < 420 ? 12 : 6"
                    v-for="(item, indexMenuKey) in setupItem[
                      selectedMenu.menuKey
                    ]"
                  >
                    <v-tooltip text="Tooltip" location="bottom">
                      <template v-slot:activator="{ props }">
                        <v-card
                          v-bind="props"
                          @click.prevent="
                            item.isActive
                              ? clickOpenDialog(
                                  item,
                                  indexMenuKey,
                                  selectedMenu.menuKey
                                )
                              : ``
                          "
                          class="rounded-xl"
                          :class="item.isActive ? `hover-card` : ``"
                          :elevation="!item.isActive ? 0 : 4"
                          :style="{
                            minHeight: `144.73px`,
                            border: !item.isActive ? `solid 1px lightgrey` : ``,
                            cursor: !item.isActive ? `unset` : `pointer`,
                          }"
                        >
                          <v-card-title>
                            <div
                              :style="{
                                display: `flex`,
                                justifyContent: `space-between`,
                                alignItems: `center`,
                              }"
                            >
                              <div>
                                <v-switch
                                  hide-details
                                  v-model="item.isActive"
                                  :color="`#15d766`"
                                  @click.stop
                                />
                              </div>
                              <v-btn
                                :size="`x-small`"
                                variant="plain"
                                icon
                                @click="
                                  setupItem[selectedMenu.menuKey].splice(
                                    indexMenuKey,
                                    1
                                  )
                                "
                              >
                                <v-icon
                                  :style="{
                                    fontSize: `2rem`,
                                    color: `black`,
                                  }"
                                  >mdi-close</v-icon
                                >
                              </v-btn>
                              <!-- <v-btn size="x-small" :icon="`mdi-cog`" /> -->
                            </div>
                          </v-card-title>
                          <v-card-text>
                            <div
                              :style="{
                                filter: item.isActive ? `` : `blur(1.5px)`,
                              }"
                            >
                              <div>
                                <p
                                  class="mb-3"
                                  :style="{
                                    fontWeight: `bold`,
                                    fontSize: `1rem`,
                                    whiteSpace: `nowrap`,
                                    overflow: `hidden`,
                                    textOverflow: `ellipsis`,
                                    textTransform: `capitalize`,
                                  }"
                                >
                                  {{ item.name }}
                                </p>
                              </div>
                              <div
                                :style="{
                                  whiteSpace: `nowrap`,
                                  overflow: `hidden`,
                                  textOverflow: `ellipsis`,
                                }"
                              >
                                <span>
                                  {{
                                    selectedMenu.menuKey === `defineSkill`
                                      ? item.description
                                      : item.definition
                                  }}
                                </span>
                              </div>
                            </div>
                          </v-card-text>
                        </v-card>
                      </template>
                      <div
                        :style="{
                          filter: item.isActive ? `` : `blur(1.5px)`,
                        }"
                      >
                        <span
                          :style="{
                            fontSize: `2rem`,
                            filter: item.isActive ? `` : `grayscale(1)`,
                          }"
                        >
                          {{
                            selectedMenu.menuKey === `defineSkill` ? `✨` : `🚧`
                          }}
                        </span>
                      </div>
                      <div>
                        <p
                          :style="{
                            fontWeight: `bold`,
                            textTransform: `capitalize`,
                          }"
                        >
                          {{ item.name }}
                        </p>
                        <p>
                          {{
                            selectedMenu.menuKey === `defineSkill`
                              ? item.description
                              : item.definition
                          }}
                        </p>
                      </div>
                    </v-tooltip>
                  </v-col>
                </v-row>
              </v-card-text>
              <!-- Dialog Actions -->
              <v-card-text
                class="pb-0"
                :style="{
                  display: 'flex',
                  flexDirection: windowWidth >= 501 ? 'row' : `column`,
                  alignItems: 'center',
                  justifyContent: 'space-between',
                }"
              >
                <div v-if="windowWidth >= 501">
                  <v-btn
                    :variant="`outlined`"
                    @click="clickBackToMain()"
                    :style="{ width: `90px` }"
                  >
                    Back
                  </v-btn>
                </div>
                <div v-if="windowWidth >= 501">
                  <v-btn
                    :disabled="
                      isLoadingSaveDraft ||
                      selectedMenu.menuKey === `defineChatbot`
                        ? !checkValueFilled(setupItem, selectedMenu.menuKey)
                        : checkDisabledSaveDraft
                    "
                    :loading="isLoadingSaveDraft"
                    @click="clickSaveDraft()"
                    color="primary"
                    text
                    :style="{ width: `130px` }"
                  >
                    {{ botMode === `create` ? `Create` : `Save Change` }}
                  </v-btn>
                  <v-btn
                    v-if="botMode === `edit`"
                    @click="clickPublish()"
                    :disabled="checkDisabledPublish"
                    color="#5EB491"
                    class="ml-2"
                    text
                    :style="{
                      width: `130px`,
                      filter: isPublish ? `hue-rotate(226deg)` : `none`,
                    }"
                  >
                    {{ isPublish ? `Unpublish` : `Publish` }}
                  </v-btn>
                </div>
                <div v-if="windowWidth <= 500" :style="{ width: `100%` }">
                  <v-btn
                    block
                    :disabled="
                      isLoadingSaveDraft ||
                      selectedMenu.menuKey === `defineChatbot`
                        ? !checkValueFilled(setupItem, selectedMenu.menuKey)
                        : checkDisabledSaveDraft
                    "
                    :loading="isLoadingSaveDraft"
                    @click="clickSaveDraft()"
                    color="primary"
                  >
                    {{ botMode === `create` ? `Create` : `Save Change` }}
                  </v-btn>
                </div>
                <div
                  class="mt-2"
                  v-if="windowWidth <= 500 && botMode === `edit`"
                  :style="{ width: `100%` }"
                >
                  <v-btn
                    block
                    @click="clickPublish()"
                    :disabled="checkDisabledPublish"
                    color="#5EB491"
                    :style="{
                      filter: isPublish ? `hue-rotate(226deg)` : `none`,
                    }"
                  >
                    {{ isPublish ? `Unpublish` : `Publish` }}
                  </v-btn>
                </div>
                <div
                  v-if="windowWidth <= 500"
                  class="mt-2"
                  :style="{ width: `100%` }"
                >
                  <v-btn block :variant="`outlined`" @click="clickBackToMain()">
                    Back
                  </v-btn>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          <!-- chat panel -->
          <v-col
            :cols="windowWidth > 1100 ? 6 : 12"
            class="pa-4"
            :style="{ height: `calc(100%)` }"
          >
            <v-card
              elevation="0"
              class="rounded-xl pa-2"
              :style="{
                height: `100%`,
                border: `solid 1px lightgrey`,
              }"
            >
              <div
                :style="{
                  height: `100%`,
                  display: !selectedUser || !chatSelected ? `flex` : `none`,
                  justifyContent: `center`,
                }"
              >
                <DataError
                  :message="`No Data`"
                  :subMessage="`⚠️ Guide: Please create chatbot first to unlock another setup.`"
                />
              </div>
              <ChatPanelBot
                :style="{
                  display: !selectedUser || !chatSelected ? `none` : ``,
                }"
                ref="chat_panel_ref"
                :selected-user-prop="selectedUser"
                :selected-chat-prop="chatSelected"
                :is-change="isChange"
                @snackbar="snackbarAction"
                :hideTopMenu="true"
              />
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <!--dialog-->
      <v-dialog v-model="setupDialog" max-width="500" persistent>
        <v-card
          class="rounded-xl"
          :title="
            selectedMenu.menuKey === `defineSkill`
              ? `✨ Setup skill funciton`
              : `🚧 Setup denied topic`
          "
        >
          <v-card-text
            :style="{
              maxHeight: `calc(100dvh - 124px)`,
              overflowY: `auto`,
            }"
          >
            <div
              v-if="setupDialogItem"
              v-for="(key, itemIndex) in Object.keys(setupDialogItem)"
              :key="`digitalTwinConfigDialog_itemIndex_${itemIndex}`"
            >
              <!-- name -->
              <div v-if="key === `name`">
                <div>
                  <p
                    :style="{ fontWeight: `bold`, textTransform: `capitalize` }"
                  >
                    {{ menuNamed(key) }}
                  </p>
                </div>
                <div
                  :style="{
                    display: `flex`,
                    justifyContent: `center`,
                  }"
                >
                  <v-text-field
                    density="compact"
                    variant="outlined"
                    :style="{ borderRadius: '8px', maxWidth: `500px` }"
                    v-model="setupDialogItem[key]"
                    :rules="[requiredRule({ key: key, type: `text` })]"
                  />
                </div>
              </div>
              <!-- description or definition -->
              <div v-if="key === `description` || key === `definition`">
                <div>
                  <p
                    :style="{ fontWeight: `bold`, textTransform: `capitalize` }"
                  >
                    {{ menuNamed(key) }}
                  </p>
                </div>
                <div
                  :style="{
                    display: `flex`,
                    justifyContent: `center`,
                  }"
                >
                  <v-textarea
                    density="compact"
                    variant="outlined"
                    :style="{ borderRadius: '8px', maxWidth: `500px` }"
                    v-model="setupDialogItem[key]"
                    :rules="[requiredRule({ key: key, type: `textarea` })]"
                  />
                </div>
              </div>
              <!-- type -->
              <div v-if="key === 'type'">
                <div>
                  <p
                    :style="{ fontWeight: `bold`, textTransform: `capitalize` }"
                  >
                    {{ menuNamed(key) }}
                  </p>
                  <p
                    v-if="setupDialogItem[key]"
                    :style="{
                      color: `#ff8d6a`,
                      fontSize: `0.7rem`,
                    }"
                  >
                    <span :style="{ fontWeight: `bold` }">⚠️ Please note:</span>
                    Changing the type will reset options.
                  </p>
                </div>
                <div
                  :style="{
                    display: `flex`,
                    justifyContent: `center`,
                  }"
                >
                  <v-autocomplete
                    v-model="setupDialogItem[key]"
                    :rules="[requiredRule({ key: key, type: `textarea` })]"
                    :items="
                      selectedMenu.menuKey === `defineSkill`
                        ? typeItem.skillType
                        : typeItem.guardType
                    "
                    variant="outlined"
                    density="compact"
                    :style="{ borderRadius: '8px', maxWidth: `500px` }"
                  />
                </div>
              </div>
              <!-- options -->
              <div
                v-if="
                  key === 'options' &&
                  setupDialogItem.type &&
                  setupDialogItem.type.trim().length > 0
                "
              >
                <div>
                  <p
                    :style="{ fontWeight: `bold`, textTransform: `capitalize` }"
                  >
                    {{ menuNamed(key) }}
                  </p>
                </div>
                <div
                  :style="{
                    display: `flex`,
                    justifyContent: `center`,
                  }"
                >
                  <v-card
                    elevation="0"
                    class="pb-0"
                    :style="{
                      width: `100%`,
                      height: `310px`,
                      overflowY: `auto`,
                      border: `solid 1px #ababab`,
                    }"
                  >
                    <div class="pl-6 py-4" v-if="!checkIsFixedOption">
                      <v-btn
                        @click="clickAddOption()"
                        class="rounded-xl"
                        :color="`#5EB491`"
                        :size="`small`"
                        variant="outlined"
                      >
                        Add options
                        <v-icon class="ml-2">mdi-plus-circle</v-icon>
                      </v-btn>
                    </div>
                    <div
                      v-for="(item, idx) in setupDialogItem[key]"
                      :key="`digitalTwinConfigDialog_options_${idx}_${setupDialogItem.type}`"
                      class="mb-4"
                      :class="checkIsFixedOption && idx === 0 ? `mt-4` : ``"
                      :style="{
                        display: `flex`,
                        justifyContent: `center`,
                      }"
                    >
                      <v-card
                        class="rounded-xl"
                        :style="{
                          backgroundColor: `#ededed`,
                          width: `90%`,
                        }"
                      >
                        <v-card-text class="pb-2">
                          <div
                            :style="{
                              display: `flex`,
                              justifyContent: `space-between`,
                              alignItems: `center`,
                            }"
                          >
                            <div
                              :style="{
                                whiteSpace: `nowrap`,
                                overflow: `hidden`,
                                textOverflow: `ellipsis`,
                                textTransform: `capitalize`,
                                fontWeight: `bold`,
                              }"
                            >
                              <span>
                                {{ menuNamed(setupDialogItem.type) }}
                              </span>
                            </div>
                            <v-btn
                              v-if="!checkIsFixedOption"
                              :disabled="setupDialogItem[key].length <= 1"
                              :size="`x-small`"
                              variant="plain"
                              icon
                              @click="setupDialogItem[key].splice(idx, 1)"
                            >
                              <v-icon
                                :style="{
                                  fontSize: `2rem`,
                                  color:
                                    setupDialogItem[key].length <= 1
                                      ? `lightgrey`
                                      : `#D6584D`,
                                }"
                                >mdi-close-circle</v-icon
                              >
                            </v-btn>
                          </div>
                          <div
                            class="mt-2"
                            v-for="(subKey, indexSubkey) in Object.keys(item)"
                            :key="`digitalTwin_for_options_sub_${indexSubkey}`"
                          >
                            <div v-if="item[subKey].type === `text`">
                              <v-text-field
                                :label="menuNamed(subKey)"
                                density="compact"
                                variant="outlined"
                                :style="{
                                  borderRadius: '8px',
                                  maxWidth: `500px`,
                                }"
                                v-model="
                                  setupDialogItem.options[idx][subKey].value
                                "
                                :rules="[
                                  requiredRule({
                                    key: subKey,
                                    type: `text`,
                                  }),
                                ]"
                              />
                            </div>
                            <div v-else-if="item[subKey].type === `textarea`">
                              <v-textarea
                                :label="menuNamed(subKey)"
                                density="compact"
                                variant="outlined"
                                :rows="2"
                                :style="{
                                  borderRadius: '8px',
                                  maxWidth: `500px`,
                                }"
                                v-model="
                                  setupDialogItem.options[idx][subKey].value
                                "
                                :rules="[
                                  requiredRule({
                                    key: subKey,
                                    type: `text`,
                                  }),
                                ]"
                              />
                            </div>
                            <div
                              v-else-if="item[subKey].type === `autocomplete`"
                            >
                              <v-autocomplete
                                :label="menuNamed(subKey)"
                                :items="
                                  setupDialogItem.options[idx][subKey].item
                                "
                                density="compact"
                                variant="outlined"
                                :rows="2"
                                :style="{
                                  borderRadius: '8px',
                                  maxWidth: `500px`,
                                }"
                                v-model="
                                  setupDialogItem.options[idx][subKey].value
                                "
                                :rules="[
                                  requiredRule({
                                    key: subKey,
                                    type: `autocomplete`,
                                  }),
                                ]"
                              />
                            </div>
                          </div>
                        </v-card-text>
                      </v-card>
                    </div>
                  </v-card>
                </div>
              </div>
            </div>
          </v-card-text>
          <!-- Dialog Actions -->
          <v-card-text
            class="pt-0"
            :style="{
              display: 'flex',
              flexDirection: 'row',
              alignItems: 'center',
              justifyContent: 'space-between',
            }"
          >
            <v-btn variant="text" @click="clickCloseDialog()"> Cancel </v-btn>

            <v-btn
              @click="clickApplyDialog()"
              :disabled="checkDisabledDialog"
              color="primary"
              class="ml-2"
              text
              :style="{ width: `130px` }"
            >
              Apply
            </v-btn>
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
          <v-btn
            color="white"
            text
            v-bind="attrs"
            @click="snackbarAlert = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-card-text>
  </v-card>
</template>

<script>
import ChatPanelBot from "../internalChatbot/chatPanelBot.vue";
import DataError from "../tools/dataError.vue";
import axios from "axios";

export default {
  name: "digitalTwinConfig",
  components: { DataError, ChatPanelBot },
  props: {
    item: {
      type: Object,
      default: null,
    },
    session: {
      type: Object,
      default: null,
    },
  },
  watch: {
    item: {
      handler(newVal) {
        if (newVal) {
          this.botMode = `edit`;
          this.preprocessSkillAndGuard();
        } else {
          this.botMode = `create`;
          this.menuItems.forEach((item, idx) => {
            if (idx !== 0) {
              item.disabled = true;
            }
          });
        }
      },
      deep: false,
      immediate: true,
    },
    "setupDialogItem.type": {
      handler(newValue, oldValue) {
        if (
          (newValue !== oldValue && oldValue) ||
          (!oldValue && this.setupDialogItem.options.length < 1)
        ) {
          const type =
            this.selectedMenu.menuKey === `defineSkill`
              ? `skillType`
              : this.selectedMenu.menuKey === `setupGuard`
              ? `guardType`
              : null;
          this.setupDialogItem.options = [];

          if (type && this.typeItem[type].includes(newValue)) {
            this.setupDialogItem.options.push(
              JSON.parse(
                JSON.stringify(this.typeDefaultOptions[type][newValue].default)
              )
            );
          }
        }
      },
      deep: false,
      immediate: false,
    },
  },
  computed: {
    checkDisabledDialog() {
      return false;
    },
    checkDisabledSaveDraft() {
      return false;
    },
    checkDisabledPublish() {
      return false;
    },
    checkIsFixedOption() {
      const menuType =
        this.selectedMenu.menuKey === `defineSkill`
          ? `skillType`
          : this.selectedMenu.menuKey === `setupGuard`
          ? `guardType`
          : null;

      const type = this.setupDialogItem.type;

      return this.typeDefaultOptions[menuType][type].fixed;
    },
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      botMode: `create`,
      botItem: null,
      //menu
      selectedMenu: { id: 0, menuKey: `defineChatbot` },
      menuItems: [
        {
          id: 0,
          menuKey: `defineChatbot`,
          name: `Define Chatbot`,
          icon: `👤`,
          disabled: false,
        },
        {
          id: 1,
          menuKey: `defineSkill`,
          name: `Define Skills, Tasks`,
          icon: `🤖`,
          disabled: false,
        },
        {
          id: 2,
          menuKey: `setupGuard`,
          name: `Setup Guard Rails`,
          icon: `🛡️`,
          disabled: false,
        },
      ],
      //chat
      chatSelected: null,
      selectedUser: null,
      isChange: false,
      draftItem: {
        id: null, //null for create , number for upsert
        bot_name: ``,
        prompt: ``,
        routing: ``,
        industry: ``,
        retrieve_image: false,
        knowledge_base: [],
        line_integration_uuid: ``, // null for no
        isActive: false,
        defineSkill: [],
        setupGuard: [],
      },
      //item
      setupItem: {
        defineChatbot: {
          bot_name: {
            id: 1,
            key: `bot_name`,
            description: "What would you like to name me?",
            type: "text",
            value: "",
          },
          prompt: {
            id: 2,
            key: `prompt`,
            description: "What do you want me to say to the user?",
            type: "textarea",
            value: "",
          },
          routing: {
            id: 3,
            key: `routing`,
            description:
              "How would you like me to respond? (e.g., mastery, friendly, formal)",
            type: "text",
            value: "",
          },
          industry: {
            id: 4,
            key: `industry`,
            description:
              "In which industry do you need me to work? (e.g., Technology, Customer Support)",
            type: "autocomplete",
            value: "",
            item: [],
          },
          retrieve_image: {
            key: `retrieve_image`,
            id: 5,
            description: "Should I be able to retrieve images? (Yes/No)",
            type: "boolean",
            value: false,
          },
          knowledge_base: {
            key: `knowledge_base`,
            id: 6,
            description:
              "Where should I pull my information from? *not required",
            type: "autocomplete-multiple",
            value: [],
            item: [],
          },
          line_integration_uuid: {
            key: `line_integration_uuid`,
            id: 7,
            description: "Do you want me connected to LINE? (Yes/No)",
            type: "autocomplete",
            value: "",
            item: [],
          },
          isActive: {
            key: `isActive`,
            id: 8,
            description:
              "Should I be active and available for responses? (Yes/No)",
            type: "boolean",
            value: true,
          },
        },
        defineSkill: [],
        setupGuard: [],
      },
      isPublish: false,
      typeDefaultOptions: null,
      typeItem: {
        skillType: [],
        guardType: [],
      },
      setupDialog: false,
      setupDialogItem: {
        name: ``,
        description: ``,
        isActive: false,
        type: null,
        options: [],
      },
      setupDialogItemIndex: 0,
      setupDialogMode: `create`,
      //snackbar
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: "untitled",
      //isLoading
      errorMsgSaveDraft: `untitled`,
      isLoadingSaveDraft: false,
      isErrorSaveDraft: true,
    };
  },
  beforeMount() {
    this.getDefineChatbotItem();
  },
  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    getDefineChatbotItem() {
      // industry
      axios
        .get(`api/chat_center/list_industry/`)
        .then((res) => {
          this.setupItem.defineChatbot.industry.item = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
      // knowledge base
      axios
        .get(`api/chat_center/list_knowledge_base/`)
        .then((res) => {
          this.setupItem.defineChatbot.knowledge_base.item = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
      // line integration
      axios
        .get(`api/chat_center/list_line_integration/`)
        .then((res) => {
          this.setupItem.defineChatbot.line_integration_uuid.item = res.data;
          this.setupItem.defineChatbot.line_integration_uuid.item.unshift({
            uuid: "No",
            user_id: "No",
            username: "No",
          });
        })
        .catch((err) => {
          console.log(err);
          this.setupItem.defineChatbot.line_integration_uuid.item.unshift({
            uuid: "No",
            user_id: "No",
            username: "No",
          });
        });
    },
    preprocessSkillAndGuard() {
      //1. skill and guard type default
      // this.typeDefaultOptions = {
      //   skillType: {
      //     football_skill: {
      //       fixed: false,
      //       default: {
      //         plan_name: { value: ``, type: `text` },
      //         plan_description: { value: ``, type: `textarea` },
      //       },
      //     },
      //   },
      //   guardType: {
      //     pharses_guard: {
      //       fixed: false,
      //       default: { word: { value: ``, type: `text` } },
      //     },
      //     harmful_content: {
      //       fixed: true,
      //       default: {
      //         hate: {
      //           value: ``,
      //           type: `autocomplete`,
      //           item: [`none`, `low`, `mid`, `high`],
      //         },
      //         insult: {
      //           value: ``,
      //           type: `autocomplete`,
      //           item: [`none`, `low`, `mid`, `high`],
      //         },
      //         sexuals: {
      //           value: ``,
      //           type: `autocomplete`,
      //           item: [`none`, `low`, `mid`, `high`],
      //         },
      //       },
      //     },
      //   },
      // };

      //2. setup default type
      // this.setSkillTypeItems();

      //3.1 defineSkill
      // this.setupItem.defineSkill = [
      //   {
      //     name: `football knowledge`,
      //     description: `Pep Guardiola knowledge in chatbot.`,
      //     isActive: false,
      //     type: `football_skill`,
      //     options: [
      //       {
      //         plan_name: { value: `4-3-2-1`, type: `text` },
      //         plan_description: {
      //           value: `Trible champ plan 2022-2023`,
      //           type: `textarea`,
      //         },
      //       },
      //     ],
      //   },
      // ];
      //3.2 setupGuard
      // this.setupItem.setupGuard = [
      //   {
      //     name: `pharses guard`,
      //     definition: `blocking hate speech to chatbot.`,
      //     isActive: false,
      //     type: `pharses_guard`,
      //     options: [
      //       {
      //         word: { value: `where is my salary.`, type: `text` },
      //       },
      //     ],
      //   },
      //   {
      //     name: `harmful guard`,
      //     definition: `blocking sexual messages.`,
      //     isActive: false,
      //     type: `harmful_content`,
      //     options: [
      //       {
      //         hate: {
      //           value: `mid`,
      //           type: `autocomplete`,
      //           item: [`none`, `low`, `mid`, `high`],
      //         },
      //         insult: {
      //           value: `mid`,
      //           type: `autocomplete`,
      //           item: [`none`, `low`, `mid`, `high`],
      //         },
      //         sexuals: {
      //           value: `mid`,
      //           type: `autocomplete`,
      //           item: [`none`, `low`, `mid`, `high`],
      //         },
      //       },
      //     ],
      //   },
      // ];

      //4. unlock skill setup and guard setup
      this.menuItems.forEach((item, idx) => {
        if (idx !== 0) {
          // unlock below
          // item.disabled = false;
          // locked for demo
          item.disabled = true;
        }
      });

      //5. get old data to setup
      axios
        .post(`api/chat_center/get_chatbot_data_new/`, { id: this.item.id })
        .then((res) => {
          Object.keys(res.data).forEach((key) => {
            if (key === `isPublish`) {
              this.isPublish = res.data[key];
            } else if (
              key !== `id` &&
              key !== `img` &&
              key !== `defineSkill` &&
              key !== `setupGuard`
            ) {
              if (key === `line_integration_uuid` && !res.data[key]) {
                this.setupItem.defineChatbot[key].value = `No`;
              } else {
                this.setupItem.defineChatbot[key].value = res.data[key];
              }
            }
          });
        })
        .catch((err) => {
          this.$emit(`catchEditErr`, err);
        });

      //6. unlock chat panel by setup botItem and botSession

      this.selectedUser = this.item;
      if (this.session) {
        this.chatSelected = this.session;
      } else {
        //get session by id
        axios
          .post(`api/chat_center/list_save_draft_session/`, {
            id: this.item.id,
          })
          .then((res) => {
            this.chatSelected = res.data[0];
          })
          .catch((err) => {
            this.$emit(`catchEditErr`, err);
          });
      }
      this.isChange = !this.isChange;
    },
    // resposive
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    setSkillTypeItems() {
      Object.keys(this.typeDefaultOptions).forEach((key) => {
        Object.keys(this.typeDefaultOptions[key]).forEach((subKey) => {
          this.typeItem[key].push(subKey);
        });
      });
    },
    menuNamed(string) {
      let name = string.replaceAll(`_`, ` `);
      if (name.length > 0) {
        name = name.charAt(0).toUpperCase() + name.slice(1);
      }
      return name;
    },
    requiredRule(item) {
      return item.type !== "boolean"
        ? (v) => !!v || `${item.key} is required.`
        : true;
    },
    clickBackToMain() {
      this.$emit(`backToMain`);
    },
    checkValueFilled(setupItem, key) {
      if (!setupItem[key]) {
        return false;
      }

      const targetObject = setupItem[key];

      for (const itemKey in targetObject) {
        if (targetObject.hasOwnProperty(itemKey)) {
          const item = targetObject[itemKey];

          if (item && item.value !== undefined) {
            const value = item.value;
            const type = item.type;

            if (
              type === "text" ||
              type === "textarea" ||
              type === "autocomplete"
            ) {
              if (typeof value !== "string" || value.trim() === "") {
                // console.warn(`Field "${itemKey}" in "${key}" is not filled.`);
                return false;
              }
            }
            // else if (type === "autocomplete-multiple") {
            //   if (!Array.isArray(value) || value.length === 0) {
            //     // console.warn(`Field "${itemKey}" in "${key}" is not filled.`);
            //     return false;
            //   }
            // }
          } else {
            // console.warn(
            //   `Field "${itemKey}" in "${key}" does not have 'value' property.`
            // );
            return false;
          }
        }
      }

      return true;
    },
    clickOpenDialog(item, idx, type) {
      if (!item) {
        this.setupDialogMode = `create`;
        this.setupDialogItem =
          type === `defineSkill`
            ? {
                name: ``,
                description: ``,
                isActive: false,
                type: null,
                options: [],
              }
            : {
                name: ``,
                definition: ``,
                isActive: false,
                type: null,
                options: [],
              };
      } else {
        this.setupDialogMode = `edit`;
        this.setupDialogItem = JSON.parse(JSON.stringify(item));
        this.setupDialogItemIndex = idx;
      }
      this.setupDialog = true;
    },
    clickCloseDialog() {
      this.setupDialog = false;
      this.setupDialogItem = {
        name: ``,
        description: ``,
        isActive: false,
        type: ``,
        options: [],
      };
    },
    clickApplyDialog() {
      if (this.setupDialogMode === `edit`) {
        this.setupItem[this.selectedMenu.menuKey][this.setupDialogItemIndex] =
          JSON.parse(JSON.stringify(this.setupDialogItem));
      } else if (this.setupDialogMode === `create`) {
        this.setupItem[this.selectedMenu.menuKey].unshift(this.setupDialogItem);
      }
      this.clickCloseDialog();
    },
    clickAddOption() {
      const type =
        this.selectedMenu.menuKey === `defineSkill`
          ? `skillType`
          : this.selectedMenu.menuKey === `setupGuard`
          ? `guardType`
          : null;
      if (type) {
        this.setupDialogItem.options.unshift(
          JSON.parse(
            JSON.stringify(
              this.typeDefaultOptions[type][this.setupDialogItem.type].default
            )
          )
        );
      }
    },
    async clickSaveDraft() {
      if (this.selectedMenu.menuKey === `defineChatbot`) {
        let draftBody = await this.getSaveDraft(
          this.botMode === `create` ? null : this.selectedUser.id
        );
        draftBody.isPublish = false;
        this.isLoadingSaveDraftSaveDraft = false;
        this.isLoadingSaveDraft = true;
        this.isErrorSaveDraft = false;
        axios
          .post(`api/chat_center/save_draft/`, {
            ...draftBody,
          })
          .then((res) => {
            this.isLoadingSaveDraft = false;
            this.isErrorSaveDraft = false;
            //when response from api
            this.$emit(`callbackNewSaveDraft`, {
              botItem: res.data.botItem,
              botSession: res.data.botSession,
            });
            this.snackbarAction({
              snackbarMsg: `Bot has been ${this.botMode}${
                this.botMode === `create` ? `d` : `ed`
              } successfully!`,
              snackbarSuccess: true,
              snackbarAlert: true,
            });
          })
          .catch((err) => {
            this.errorMsgSaveDraft = err;
            this.isLoadingSaveDraft = false;
            this.isErrorSaveDraft = true;
          });
        console.log(this.setupItem);
      } else if (this.selectedMenu.menuKey === `defineSkill`) {
      } else if (this.selectedMenu.menuKey === `setupGuard`) {
      }
      console.log("click save draft");
    },
    clickPublish() {
      axios
        .post(`api/chat_center/chatbot_publish/`, { id: this.selectedUser.id })
        .then(() => {
          this.snackbarAction({
            snackbarMsg: `Your chatbot has been successfully published!`,
            snackbarSuccess: true,
            snackbarAlert: true,
          });
          this.clickBackToMain();
        })
        .catch((err) => {
          this.snackbarAction({
            snackbarMsg: err,
            snackbarSuccess: false,
            snackbarAlert: true,
          });
        });
    },
    snackbarAction(item) {
      this.snackbarMsg = item.snackbarMsg;
      this.snackbarSuccess = item.snackbarSuccess;
      this.snackbarAlert = item.snackbarAlert;
    },
    getSaveDraft(id) {
      this.draftItem = {
        id: null, //null for create , number for upsert
        bot_name: ``,
        prompt: ``,
        routing: ``,
        industry: ``,
        retrieve_image: false,
        knowledge_base: [],
        line_integration_uuid: ``, // null for no
        isActive: false,
        defineSkill: [],
        setupGuard: [],
      };
      this.draftItem.id = id;
      this.draftItem.bot_name = this.setupItem.defineChatbot.bot_name.value;
      this.draftItem.prompt = this.setupItem.defineChatbot.prompt.value;
      this.draftItem.routing = this.setupItem.defineChatbot.routing.value;
      this.draftItem.industry =
        this.setupItem.defineChatbot.industry.value === `No`
          ? null
          : this.setupItem.defineChatbot.industry.value;
      this.draftItem.retrieve_image =
        this.setupItem.defineChatbot.retrieve_image.value;
      this.draftItem.knowledge_base =
        this.setupItem.defineChatbot.knowledge_base.value;
      this.draftItem.line_integration_uuid =
        this.setupItem.defineChatbot.line_integration_uuid.value === `No`
          ? null
          : this.setupItem.defineChatbot.line_integration_uuid.value;
      this.draftItem.isActive = this.setupItem.defineChatbot.isActive.value;
      this.draftItem.defineSkill = this.setupItem.defineSkill;
      this.draftItem.setupGuard = this.setupItem.setupGuard;
      return this.draftItem;
    },
  },
};
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}
</style>
