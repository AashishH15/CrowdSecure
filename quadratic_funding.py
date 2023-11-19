def getAccountBalance(totalFunds, ADonors, BDonors, CDonors):
    totalDonors = ADonors + BDonors + CDonors
    projectA = (ADonors/totalDonors)*(totalFunds)
    projectB = (BDonors/totalDonors)*(totalFunds)
    projectC = (CDonors/totalDonors)*(totalFunds)

    return projectA, projectB, projectC


