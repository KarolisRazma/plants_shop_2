import express from 'express';
import { Position, Workplace } from '../tools/database.js';
import errorTemplate from '../tools/error.js';

const router = express.Router();

router.get('/', async (req, res) => {
    await Workplace.find().then(results => {
        if (results.length > 0) {
            res.status(200);
            res.send(results);
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No workplaces found!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    });
});

router.post('/', async (req, res) => {
    let lastID = 0;
    await Workplace.findOne().sort({ _id: -1 }).limit(1).then(result => {
        lastID = result.toJSON()._id;
    }).catch(err => {
        lastID = 0;
    });

    let workplace = new Workplace({
        _id: lastID + 1,
        companyName: req.body.companyName || "",
        description: req.body.description || "",
        industry: req.body.industry || "",
        website: req.body.website || "",
        specialities: req.body.specialities || [],
        refPositions: `/workplaces/${lastID + 1}/positions`
    });

    if (!workplace.validateSync()) {
        await workplace.save().then(result => {
            res.status(201);
            res.location(`workplaces/${workplace._id}`);
            res.send(result);
        }).catch(err => {
            res.status(500);
            res.send(errorTemplate(500, 'Failed to collect data!'));
        });
    } else {
        res.status(400);
        res.send(errorTemplate(400, 'To create resource compnayName is needed!'));
    }
});

router.get('/:id', async (req, res) => {
    await Workplace.findOne({ _id: req.params.id }).then(result => {
        if (result !== null) {
            res.status(200);
            res.send(result);
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No workplaces found!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    });
});

router.put('/:id', async (req, res) => {
    let workplace = new Workplace({
        _id: req.params.id,
        companyName: req.body.companyName,
        description: req.body.description,
        industry: req.body.industry,
        website: req.body.website,
        specialities: req.body.specialities
    });

    await Workplace.findOneAndUpdate({ _id: req.params.id }, workplace, { new: true }).then(result => {
        if (result !== null) {
            res.status(200);
            res.location(`/workplaces/${req.params.id}`);
            res.send(result);
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No workplaces found for updation!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    });
});

router.delete('/:id', async (req, res) => {
    let length = 0;
    await Workplace.findOneAndRemove({ _id: req.params.id }).then(result => {
        if (result) {
            res.status(204);
            res.send('');
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No workplaces found for deletion!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    });
    await Position.find({ workplaceId: req.params.id }).then(result => {
        length = result.length;
    });

    for (let i = 0; i < length; ++i) {
        await Position.findOneAndRemove({ workplaceId: req.params.id });
    }
});

router.all('/', (req, res) => {
    res.status(405);
    res.send(errorTemplate(405, 'Method not allowed!'));
});

router.all('/:id', (req, res) => {
    res.status(405);
    res.send(errorTemplate(405, 'Method not allowed!'));
});

export default router;