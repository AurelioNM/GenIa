*** Settings ***
Resource    ../resources/common.robot
Resource   ../variables/env.robot

*** Test Cases ***
Should Interact with intation SUGGEST_PRODUCT_BASED_ON_CATEGORY Successfully
    Create Chat Session

    Execute Chat Interaction
    ...    ${SESSION_ID}
    ...    ${CUSTOMER_EMAIL}
    ...    Suggest me products on the snacks category
    Sleep    5s


Should Interact with intation SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY Successfully
    Create Chat Session

    Execute Chat Interaction
    ...    ${SESSION_ID}
    ...    ${CUSTOMER_EMAIL}
    ...    Suggest me products that match with my purchase history
    Sleep    5s


Should Interact with intation SUGGEST_DAY_AND_PRODUCTS_BASED_ON_WEATHER Successfully
    Create Chat Session

    Execute Chat Interaction
    ...    ${SESSION_ID}
    ...    ${CUSTOMER_EMAIL}
    ...    I want to go for a walk on a rainy day
    Sleep    5s


Should Interact with intation PURCHASE_PRODUCT Successfully
    Create Chat Session

    Execute Chat Interaction
    ...    ${SESSION_ID}
    ...    ${CUSTOMER_EMAIL}
    ...    I would like to buy 7 Ruffles and a Nutella
    Sleep    5s


Should Interact with intation TARANTINO_QUESTION Successfully
    Create Chat Session

    Execute Chat Interaction
    ...    ${SESSION_ID}
    ...    ${CUSTOMER_EMAIL}
    ...    Did Tarantino won the oscar? If yes, with movies?
    Sleep    5s

Should Interact with intation WISDOM_PHRASE Successfully
    Create Chat Session

    Execute Chat Interaction
    ...    ${SESSION_ID}
    ...    ${CUSTOMER_EMAIL}
    ...    Give me the wisdom of the day
    Sleep    5s

Should Interact with intation UNKNOWN Successfully
    Create Chat Session

    Execute Chat Interaction
    ...    ${SESSION_ID}
    ...    ${CUSTOMER_EMAIL}
    ...    Tell me how to do backflips
    Sleep    5s
