import species

# might need to change retrieval and retrieval utils to call poormans from petitRADTRANS.poor_mans_nonequ_chem.

# import species
species.SpeciesInit()
# set up database
database = species.Database()
database.add_companion(name='51 Eri b')
# add your object's data
database.add_object('51 Eri b',
                    distance=None,
                    app_mag=None,
                    flux_density=None,
                    spectrum={
                              'SPHERE': ('51erib_sphere_yjh.dat', None, 25.)
                             },
                    deredden=None)
# set path for output
output_folder = 'multinest'
# set up AtmosphericRetrieval object
retrieve = species.AtmosphericRetrieval(object_name='51 Eri b',
                                        line_species=['CO_all_iso', 'H2O', 'CH4', 'NH3', 'CO2', 'H2S'],
                                        # i renamed "Na_allard" to Na, "K_allard" to K, "TiO_all_Exomol" to TiO, VO_Plez to VO
                                        cloud_species=['Na2S(c)_cd', 'KCL(c)_cd'],
                                        scattering=True, #False if no clouds
                                        output_folder=output_folder,
                                        wavel_range=(0.95, 5),
                                        inc_spec=['SPHERE',],
                                        inc_phot=True,
                                        pressure_grid='smaller',#'standard' 'clouds'
                                        weights=None)
# run the retrieval
retrieve.run_multinest(bounds={'logg': (3.5, 5.5),
                               'c_o_ratio': (0.3, 1.0),
                               'metallicity': (-0.3, 1.),
                               'radius': (0.8, 1.5),
                               'fsed': (0., 10.),
                               'log_kzz': (4., 14.),
                               'na2s_fraction':(-3.,1.),
                               'kcl_fracton':(-3.,1.),
                               # 'log_tau_cloud': (-2., 1.), # if result should be cloudy but is not, set this
                               # 'fe_mgsio3_ratio': (-2., 2.),
                               # 'al2o3_mgsio3_ratio': (-2., 2.),
#                                'ism_ext': (1.7, 1.7)
                              },
                       prior={'mass':(4.0,2.0),},
                       chemistry='equilibrium',
                       quenching=None,
                       pt_profile='molliere',
#                        cross_corr=['GRAVITY'], # only if high resolution, need hr mode, lbl species in line_species
                       fit_corr=['SPHERE'],
                       n_live_points=50, #500-1000
                       resume=False, # if running on cluster/intermediate results
                       plotting=True, # testing plots
                       pt_smooth=0.)



database.add_retrieval(tag='51Erib',
                       output_folder=output_folder,
                       inc_teff=True)

database.get_retrieval_teff(tag='51Erib',
                            random=30)

outpref = '51Erib'
outpost = 'logtaucloud'

species.plot_posterior(tag='51Erib',
                       offset=(-0.3, -0.35),
                       vmr=True,
                       inc_mass=True,
                       inc_pt_param=False,
                       output=outpref+'posterior'+outpost+'.pdf')

samples, radtrans = database.get_retrieval_spectra(tag='51Erib',
                                                   random=30,
                                                   wavel_range=(0.5, 6.),
                                                   spec_res=500.)

species.plot_pt_profile(tag='51Erib',
                        random=100,
                        xlim=(0., 6000.),
                        offset=(-0.07, -0.14),
                        output=outpref+'pt_profile_grains'+outpost+'.pdf',
                        radtrans=radtrans,
                        extra_axis='grains')

species.plot_opacities(tag='51Erib',
                       offset=(-0.1, -0.14),
                       output=outpref+'opacities'+outpost+'.pdf',
                       radtrans=radtrans)

species.plot_clouds(tag='51Erib',
                    offset=(-0.1, -0.15),
                    output=outpref+'clouds'+outpost+'.pdf',
                    radtrans=radtrans,
                    composition='MgSiO3')

best = database.get_probable_sample(tag='51Erib')

objectbox = database.get_object('51 Eri b B',
                                inc_phot=True)

objectbox = species.update_spectra(objectbox, best)

residuals = species.get_residuals(datatype='model',
                                  spectrum='petitradtrans',
                                  parameters=best,
                                  objectbox=objectbox,
                                  inc_phot=True,
                                  inc_spec=True,
                                  radtrans=radtrans)

modelbox = radtrans.get_model(model_param=best,
                              spec_res=500.,
                              plot_contribution=outpref+'contribution'+outpost+'.pdf')

no_clouds = best.copy()
no_clouds['log_tau_cloud'] = -100.
# no_clouds['mgsio3_fraction'] = -100.
# no_clouds['fe_fracton'] = -100.
model_no_clouds = radtrans.get_model(no_clouds)

species.plot_spectrum(boxes=[samples, modelbox,
                             model_no_clouds,
                             objectbox],
                      filters=None,
                      plot_kwargs=[{'zorder':3,'ls': '-', 'lw': 0.1, 'color': 'gray'},
                                   {'zorder':3,'ls': '-', 'lw': 0.5, 'color': 'black'},
                                   {'zorder':3,'ls': '--', 'lw': 0.3, 'color': 'black'},
                                   {
                                    'SPHERE': {'zorder':1,'marker': '', 'ms': 5., 'mew': 0., 'color': '#5f61b4', 'ls': 'none', 'capsize':2, 'alpha': 1, 'label': 'VLT/SPHERE'},
                                    }],
                      residuals=residuals,
                      xlim=(0.95, 2.5),
                      # ylim=(0.15e-16, 1.15e-15),
                      ylim_res=(-5., 5.),
                      scale=('linear', 'linear'),
                      offset=(-0.6, -0.05),
                      figsize=(12, 6),
                      legend=[{'loc': 'upper right', 'fontsize': 8.}, {'loc': 'lower left', 'fontsize': 8.}],
                      output=outpref+'spectrum'+outpost+'.pdf')
