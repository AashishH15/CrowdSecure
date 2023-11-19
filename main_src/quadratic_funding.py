def getQuadFunding(totalFunds, ADonors, BDonors, CDonors):
    totalDonors = ADonors + BDonors + CDonors

    if totalDonors == 0:
        return 0, 0, 0
    
    projectA = (ADonors/totalDonors)*(totalFunds)
    projectB = (BDonors/totalDonors)*(totalFunds)
    projectC = (CDonors/totalDonors)*(totalFunds)

    return projectA, projectB, projectC