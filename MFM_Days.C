#include <TMath.h>
#include <iostream>

using namespace std;
double days(double delta_z, double delta_theta, double delta_r){

    double v_z = 5.0; //Unit : mm/s
    double v_r = 5.0; //Unit : mm/s
    double v_theta = 1./9.; //Unit : rad/s
    double r_scan = (delta_r/v_r) * (900/delta_r) + delta_theta/v_theta; // scan along r and rotate one step in theta
    double theta_scan = (r_scan * 2*TMath::Pi()/delta_theta) + delta_z/v_z; //rotate along theta and move one step in z
    double z_scan = theta_scan * (3220/delta_z) - delta_z/v_z;//rotate along theta and move along z

    double points = (3220/delta_z) * (900/delta_r) * (2*TMath::Pi()/delta_theta);
    double total_days = (z_scan + 7.5 * points)/(24*60*60);
    cout<< "Moving time : " << z_scan/(24*60*60) << " days"<< endl;
    cout<< "DAQ time : " << (points * 7.5)/(24*60*60) << " days"<< endl;

    return total_days;
}
